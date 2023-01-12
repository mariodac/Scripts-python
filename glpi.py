# Desenvolvido  em 19/04/2022
# Atualização: 9/04/2022.
# Loga no GLPI e realiza cadastra de categoria

import getpass
import re
from time import sleep

import selenium.webdriver.chrome.options as chromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


def optionsChrome(headless=False):
    """ Configura opções para chrome """
    chrome_options = chromeOptions.Options()
    print('Configurando navegador Chrome ...')
    if(headless):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    return chrome_options


def open_glpi(url: str, dic: dict):
    s = Service(ChromeDriverManager().install())
    with webdriver.Chrome(service=s, options=optionsChrome()) as driver:
        driver.get(url)
        alert = 'alerta'
        while alert:
            user = input('User: ')
            password = getpass.getpass('Password: ')
            login_element = driver.find_element(By.ID, 'login_name')
            password_element = driver.find_element(By.ID, 'login_password')
            login_element.send_keys(user)
            password_element.send_keys(password)
            btn_login = driver.find_element(By.NAME, 'submit')
            btn_login.click()
            sleep(2)
            try:
                alert = driver.find_element(By.CSS_SELECTOR, '.center.b')
            except:
                alert = None
            if alert:
                # print('Login falhou!')
                print(alert.text)
                alert.find_element(By.TAG_NAME, 'a').click()

        """ INSERT CATEGORY
            for key, value in dic.items():
            insert_category(driver, name=key, code=value[0], comment=value[1])
            for key2, value2 in value[2].items():
                insert_category(driver, name=key2, code=value2[0], comment=value2[1], child=key)
                for key3, value3 in value2[2].items():
                        insert_category(driver, name=key3, code=value3[0], comment=value3[1], child=key2) """

        # INSERE Nobreak
        insert_disp(driver, dic_nobreak["nome"], dic_nobreak["status"], dic_nobreak["local"], dic_nobreak["marca"], dic_nobreak["modelo"], dic_nobreak["comentario"], dic_nobreak["sn"])
        
         
         


def insert_category(driver: webdriver.Chrome, name: str, code: str, comment: str, child: str = None):
    driver.get('http://192.168.6.250/glpi/front/itilcategory.form.php')
    sleep(2)
    name_element = driver.find_element(By.NAME, 'name')
    code_element = driver.find_element(By.NAME, 'code')
    comment_element = driver.find_element(By.NAME, 'comment')
    name_element.send_keys(name)
    code_element.send_keys(code)
    comment_element.send_keys(comment)
    btn_add = driver.find_element(By.NAME, 'add')
    if child:
        select = driver.find_element(By.CLASS_NAME, 'select2-selection__arrow')
        select.click()
        sleep(5)
        options = driver.find_elements(By.XPATH, "//li[@role='option']")
        # options_txt = [item.text for item in options]
        for item in options:
            if re.search(child, item.text):
                item.click()
                break

    btn_add.click()

def insert_disp(driver: webdriver.Chrome, nome: str, status: str, local: str, marca: str, modelo: str, comments: str, sn: str):
   driver.get('http://192.168.6.250/glpi/front/peripheral.form.php?')
   element = driver.find_element(By.NAME, 'name')
   element.send_keys(nome)
   print
   

dic_category = {
    "Suporte de TI": [
        "1",
        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao suporte helpdesk de primeiro nível.",
        {
            "Ajuda e Suporte": [
                "1.1",
                "Categoria de chamado organizacional.",
                {
                    "Atendimento ao Usuário": [
                        "1.1.1",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao suporte básico em TI (não atendida de forma específica em \"Hardware (Dispositivos/Equipamentos)\", \"Internet e Redes\" e \"Softwares e Aplicativos\")."
                    ],
                    "Consultoria Técnica":[
                        "1.1.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a uma consultoria especializadacom um parecer técnico."
                    ],
                    "Hardware (Dispositivos/Equipamentos)":[
                        "1.1.3",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao suporte em\"Hardware (Dispositivos/Equipamentos)\"."
                    ],
                    "Internet e Redes":[
                        "1.1.4",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao suporte em \"Internet e Redes\"."
                    ],
                    "Softwares e Aplicativos":[
                        "1.1.5",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao suporte em \"Softwares e Aplicativos\""
                    ]
                }
            ],
            "Armazenamento e Servidores":[
                "1.2",
                "Categoria de chamado organizacional.",
                {
                    "Compartilhamento de Arquivos em Rede": [
                        "1.2.1",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao compartilhamento de arquivos em rede (serviço de servidor de arquivos)."
                    ],
                    "Servidores, Virtualização e Nuvem":[
                        "1.2.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a servidores físicos e/ou virtuais."
                    ]
                }
            ],
            "Ativos de TI":[
                "1.3",
                "Categoria de chamado organizacional.",
                {
                    "Ativos de Hardware": [
                        "1.3.1",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a gestão de ativos de hardware(acompanhamento do ciclo de vida de ativos de hardware – administração,gerência, controle e inventário)."
                    ],
                    "Ativos de Redes":[
                        "1.3.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a gestão de ativos de redes (acompanhamento do ciclo de vida de ativos de redes – administração, gerência, controle e inventário)."
                    ],
                    "Ativos de Software":[
                        "1.3.3",
                        "Categoria de chamado para atendimento egerenciamento de serviços relacionados a gestão de ativos de software (acompanhamento do ciclo de vida de ativos de software – administração,gerência, controle e inventário)."
                    ]
                }
            ],
            "Contas e Acessos":[
                "1.4",
                "Categoria de chamado organizacional.",
                {
                    "Acesso Remoto": [
                        "1.4.1",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados as contas e/ou acessos de usuários de modo remoto (VPN e Proxy) a recursos institucionais (acessos de fora para dentro da instituição)."
                    ],
                    "Sistemas Internos":[
                        "1.4.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados as contas e/ou acessos de usuários a recursos internos (acessos de dntro para dentro da instituição)"
                    ],
                    "Sistemas Externos":[
                        "1.4.3",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados as contas e/ou acessos de usuáriosa recursos externos (acessos de dentro para fora da instituição)."
                    ]
                }
            ],
            "E-Mail e Listas":[
                "1.5",
                "Categoria de chamado organizacional.",
                {
                    "E-Mail": [
                        "1.5.1",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados ao aliase de e-mail."
                    ],
                    "Listas de E-mails":[
                        "1.5.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados as listas de e-mails."
                    ]
                }
            ],
            "Segurança da Informação":[
                "1.6",
                "Categoria de chamado organizacional.",
                {
                    "Auditoria e Análise": [
                        "1.6.1",
                        "Categoria de chamado para atendimento egerenciamento de serviços relacionados a processos de auditoria e análise de logs, vulnerabilidades e requisitos de segurança de sistemas."
                    ],
                    "Backup":[
                        "1.6.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a processos de backups e/ou cópias de segurançade dados institucionais."
                    ],
                    "Firewall":[
                        "1.6.3",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a processos de segurança através de firewall."
                    ],
                    "Gestão de IP Público":[
                        "1.6.4",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a gestão de IP público."
                    ],
                    "Incidentes de Segurança":[
                        "1.6.5",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a processos de incidentes de segurança."
                    ],
                    "Monitoramento":[
                        "1.6.6",
                        "Categoria de chamado para atendimento egerenciamento de serviços relacionados a processos de monitoramento."
                    ]
                }
            ]
        }
    ],
    "Serviços Gerais": [
        "2",
        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a equipe de manutenção e/ou terceiros.",
        {
            "Refrigeração": [
                "2.1",
                "Categoria de chamado organizacional.",
                {
                    "Ar-condicionado": [
                        "2.1.1",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a ar-condicionado. (Manutenções, instalações)."
                    ],
                    "Climatizador":[
                        "2.1.2",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a climatizador. (Manutenções, instalações)."
                    ],
                    "Ventilador":[
                        "2.1.3",
                        "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a ventilador. (Manutenções, instalações)."
                    ]
                }
            ],
            "Elétrica":[
                "2.2",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a instalação de rede elétrica, tomadas, lâmpadas, interruptores ..."
            ],
            "Hidráulica":[
                "2.3",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a vazamentos, troca de sifão, torneiras, vedação ..."
            ],
            "Pintura":[
                "2.4",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a pintura e revestimento."
            ],
            "Alvenaria":[
                "2.5",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a estruturas e paredes."
            ],
            "Câmeras":[
                "2.6",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a circuito interno de televisão."
            ],
            "Alarmes":[
                "2.7",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a sensores magnéticos ..."
            ],
            "Forro PVC/GESSO":[
                "2.8",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a forro de PVC, GESSO e Lages. "
            ],
            "Jardinagem":[
                "2.9",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a gramas, plantas, matos ... "
            ],
            "Montagem":[
                "2.10",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a moveis novos ou usados, regulagem de portas, gavetas, baias..."
            ],
            "Instalações":[
                "2.11",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a instalação de luminárias, prateleira, cortinas, varal, suportes, nichos ..."
            ],
            "Telhados/Calhas":[
                "2.12",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a calhas e telhas."
            ],
            "Serralheria /Soldas":[
                "2.13",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a manutenção e instalações portas, portões, janelas, grades ..."
            ],
            "Limpeza de caixa D’água":[
                "2.14",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a higienização de caixa d´água, tanques ..."
            ],
            "Dedetização":[
                "2.15",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a combate de pragas e insetos."
            ],
            "Outros":[
                "2.16",
                "Categoria de chamado para atendimento e gerenciamento de serviços relacionados a outros tipos de serviços"
            ]
        }
    ]
}

dic_micro = {
    "MICRO-01": {
        "status": "Ativo",
        "nome": "MICRO-01",
        "local": "Anexo Lateral -> Cozinha",
        "marca": "Consul",
        "modelo": "CM020BFBNA"
    },
    "MICRO-02": {
        "status": "Ativo",
        "nome": "MICRO-02",
        "local": "Anexo Lateral -> Cozinha",
        "marca": "LG",
        "modelo": "MS2355RA"
    },
    "MICRO-03": {
        "status": "Ativo",
        "nome": "MICRO-03",
        "local": "Anexo Frontal -> Area de descanso",
        "marca": "PANASONIC",
        "modelo": "NN-ST254WRUK"
    "MICRO-04": {
        "status": "Manutenção",
        "nome": "MICRO-04",
        "local": "Sem localização",
        "marca": "Midea",
        "modelo": "MTAE22"
    },
    "MICRO-05": {
        "status": "Danificado",
        "nome": "MICRO-05",
        "local": "Anexo Lateral -> Oficina TI",
        "marca": "Electrolux",
        "modelo": "MEF30"
    }

}
dic_nobreak = {
  "status": "Ativo",
  "nome": "NOB-19",
  "local": "Prédio Principal > 001-Determinação",
  "marca": "SMS",
  "modelo": "UST3200BI",
  "comentario": "Potência: 3KVA"
}

open_glpi('http://192.168.6.250/glpi/front/login.php', dic_nobreak)
