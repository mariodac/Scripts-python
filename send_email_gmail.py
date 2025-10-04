"""
SMTP + IMAP (Gmail) — Enviar e marcar como Importante (sem Gmail API).
- Envia via SMTP (smtplib)
- Localiza a mensagem via IMAP pelo Message-ID (X-GM-RAW rfc822msgid:...)
- Aplica a label de Importante com +X-GM-LABELS (Important)

Pré-requisitos:
1) Ative IMAP no Gmail: Configurações → Encaminhamento e POP/IMAP → Habilitar IMAP
2) Ative 2FA e crie uma "App Password" para usar no SMTP/IMAP
3) Preencha as constantes USER, APP_PASSWORD e os campos de mensagem abaixo.

Observação:
- Este script usa apenas bibliotecas padrão do Python (smtplib, imaplib, ssl, email).
- Gmail pode demorar alguns segundos para disponibilizar a mensagem via IMAP após o envio.
"""

import smtplib
import ssl
import imaplib
import time
import re, os
from typing import Optional
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid, formatdate

load_dotenv()
# ============ CONFIGURAÇÕES ============
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993

# Credenciais da conta Gmail (use App Password com 2FA)
USER = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("EMAIL_PASSWORD") # NÃO use sua senha normal

# Dados do e-mail a enviar
TO = os.getenv("TO_EMAIL")
SUBJECT = "[Teste] SMTP + IMAP marcando como Importante"
HTML_BODY = "<p>Olá! Este e-mail foi enviado via SMTP e marcado como <b>Importante</b> via IMAP.</p>"
TEXT_BODY = "Olá! Este e-mail foi enviado via SMTP e marcado como Importante via IMAP."

# Tempo máximo para aguardar o e-mail aparecer no IMAP (segundos)
IMAP_APPEAR_TIMEOUT = 30
IMAP_APPEAR_INTERVAL = 2  # intervalo entre tentativas


# ============ SMTP ============
def send_email_and_get_msgid() -> str:
    """
    Envia o e-mail via SMTP com um Message-ID próprio e retorna esse Message-ID.
    """
    msg = MIMEMultipart("alternative")
    msg_id = make_msgid()  # ex.: '<20251004.abc123@host>'
    msg["Message-ID"] = msg_id
    msg["Date"] = formatdate(localtime=True)
    msg["From"] = USER
    msg["To"] = TO
    msg["Subject"] = SUBJECT

    # Cabeçalhos de prioridade (clientes respeitam; não aplicam a label do Gmail por si)
    msg["Importance"] = "high"
    msg["X-Priority"] = "1"

    msg.attach(MIMEText(TEXT_BODY, "plain", "utf-8"))
    msg.attach(MIMEText(HTML_BODY, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(USER, APP_PASSWORD)
        server.sendmail(USER, [TO], msg.as_string())

    return msg_id  # com < >


# ============ IMAP helpers ============
LIST_RE = re.compile(br'\((?P<flags>[^\)]*)\)\s+"(?P<delim>[^"]+)"\s+(?P<name>.+)')

def list_mailboxes_raw(imap: imaplib.IMAP4_SSL) -> list[bytes]:
    typ, mailboxes = imap.list()
    if typ != "OK" or mailboxes is None:
        return []
    return mailboxes

def find_mailbox_with_attr_bytes(imap: imaplib.IMAP4_SSL, attr: bytes) -> Optional[bytes]:
    """
    Retorna o NOME DA MAILBOX exatamente como o servidor envia (bytes, possivelmente com aspas),
    cuja linha de LIST contenha o atributo IMAP (ex.: b'\\All', b'\\Sent', b'\\Inbox').
    """
    mailboxes = list_mailboxes_raw(imap)
    for raw in mailboxes:
        m = LIST_RE.match(raw)
        if not m:
            continue
        flags = m.group("flags")  # bytes, ex: b'\\HasNoChildren \\All'
        name_quoted = m.group("name")  # bytes, ex: b'"[Gmail]/All Mail"'
        if attr in flags.split():
            return name_quoted  # já vem com aspas — perfeito para SELECT
    return None

def select_mailbox_bytes(imap: imaplib.IMAP4_SSL, mailbox_quoted_bytes: bytes) -> None:
    """
    Faz SELECT usando o nome em bytes exatamente como veio do LIST (com aspas).
    """
    typ, _ = imap.select(mailbox_quoted_bytes, readonly=False)
    if typ != "OK":
        raise RuntimeError(f"Não foi possível selecionar a mailbox: {mailbox_quoted_bytes!r}")


def wait_for_message_in_imap(imap: imaplib.IMAP4_SSL, msg_id: str) -> Optional[bytes]:
    """
    Aguarda até IMAP_APPEAR_TIMEOUT para a mensagem aparecer no IMAP.
    Busca usando X-GM-RAW (rfc822msgid:RID) e, se necessário, por cabeçalho Message-ID.
    Retorna o UID (bytes) se encontrar; None se não aparecer no tempo limite.
    """
    rid = msg_id.strip("<>")
    deadline = time.time() + IMAP_APPEAR_TIMEOUT

    while time.time() < deadline:
        # 1) Tenta com X-GM-RAW (busca estilo Gmail)
        typ, data = imap.uid("SEARCH", None, "X-GM-RAW", f"rfc822msgid:{rid}")
        if typ == "OK" and data and data[0]:
            uids = data[0].split()
            if uids:
                return uids[-1]

        # 2) Fallback: busca por cabeçalho Message-ID
        typ, data = imap.uid("SEARCH", None, "HEADER", "Message-ID", msg_id)
        if typ == "OK" and data and data[0]:
            uids = data[0].split()
            if uids:
                return uids[-1]

        time.sleep(IMAP_APPEAR_INTERVAL)

    return None


def imap_mark_important_by_msgid(msg_id: str) -> None:
    """
    Conecta no IMAP, encontra a mensagem pelo Message-ID e aplica a label de Importante.
    Usa a busca X-GM-RAW 'rfc822msgid:' do Gmail (com fallback por HEADER).
    """
    imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    try:
        imap.login(USER, APP_PASSWORD)

        # Diagnóstico opcional: listar mailboxes raw
        # for raw in list_mailboxes_raw(imap):
        #     print(raw)

        # Preferir "All Mail" (\All). Se não houver, usar "Sent" (\Sent). Se falhar, INBOX.
        mailbox = find_mailbox_with_attr_bytes(imap, b'\\All')
        if not mailbox:
            mailbox = find_mailbox_with_attr_bytes(imap, b'\\Sent')
        if not mailbox:
            mailbox = b'INBOX'  # INBOX geralmente ASCII simples

        select_mailbox_bytes(imap, mailbox)

        uid = wait_for_message_in_imap(imap, msg_id)
        if not uid:
            raise RuntimeError("Mensagem não encontrada no IMAP dentro do tempo limite. "
                               "Tente aumentar IMAP_APPEAR_TIMEOUT ou verifique a mailbox selecionada.")

        # Aplica a label de IMPORTANTE (especial do Gmail)
        typ, _ = imap.uid("STORE", uid, "+X-GM-LABELS", r"(\Important)")
        if typ != "OK":
            raise RuntimeError("Não foi possível aplicar a label \\Important via IMAP.")

    finally:
        try:
            imap.close()
        except Exception:
            pass
        imap.logout()


def main():
    print("Enviando e-mail via SMTP...")
    msg_id = send_email_and_get_msgid()
    print(f"OK. Message-ID: {msg_id}")

    print("Conectando via IMAP e marcando como Importante...")
    imap_mark_important_by_msgid(msg_id)
    print("Concluído: mensagem marcada como Importante.")

if __name__ == "__main__":
    main()
