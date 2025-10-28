import argparse
import os
import sys
import tempfile
from io import BytesIO

# PDF leitura/detecção de texto
import fitz  # PyMuPDF

# Conversão PDF -> DOCX
from pdf2docx import Converter

# OCR fallback
from pdf2image import convert_from_path
import pytesseract
from pypdf import PdfWriter, PdfReader


def has_selectable_text(pdf_path: str, sample_pages: int = 10, min_ratio: float = 0.3) -> bool:
    """
    Retorna True se o PDF aparenta ter texto selecionável na proporção mínima indicada.
    Amostra até 'sample_pages' páginas para ser rápido em PDFs grandes.
    """
    with fitz.open(pdf_path) as doc:
        total = min(len(doc), sample_pages)
        with_text = 0
        for i in range(total):
            page = doc.load_page(i)
            txt = page.get_text("text") or ""
            if txt.strip():
                with_text += 1
        ratio = (with_text / total) if total > 0 else 0.0
        return ratio >= min_ratio


def ocr_pdf_with_tesseract(
    pdf_path: str,
    out_pdf_path: str,
    lang: str = "por+eng",
    poppler_bin: str | None = None,
    dpi: int = 300,
    tesseract_cmd: str | None = None,
) -> None:
    """
    Fallback de OCR puro em Python (sem OCRmyPDF):
    1) Converte páginas do PDF em imagens
    2) Roda Tesseract e gera um PDF pesquisável por página
    3) Junta todas as páginas em 'out_pdf_path'
    """
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    # 1) PDF -> imagens
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_bin)

    # 2) Página a página: imagem -> PDF com camada de texto (Tesseract)
    writer = PdfWriter()
    for idx, img in enumerate(images, start=1):
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf", lang=lang)
        page_pdf = PdfReader(BytesIO(pdf_bytes))
        # Append todas as páginas geradas (normalmente 1)
        for p in page_pdf.pages:
            writer.add_page(p)

    # 3) Salva PDF final com texto pesquisável
    with open(out_pdf_path, "wb") as f:
        writer.write(f)


def pdf_to_docx(pdf_path: str, out_docx_path: str, start: int = 0, end: int | None = None) -> None:
    """
    Converte PDF (nativo ou com camada OCR) em DOCX preservando o máximo do layout/imagens.
    """
    cv = Converter(pdf_path)
    try:
        cv.convert(out_docx_path, start=start, end=end)
    finally:
        cv.close()


def main():
    parser = argparse.ArgumentParser(
        description="Converter PDF (nativo ou escaneado) para Word (.docx), preservando texto (via OCR) e imagens."
    )
    parser.add_argument("pdf", help="Caminho do arquivo PDF de entrada")
    parser.add_argument("-o", "--output", help="Caminho do .docx de saída (padrão: mesmo nome do PDF)")
    parser.add_argument("--lang", default="por+eng", help="Idiomas do OCR Tesseract (ex.: por, eng, por+eng)")
    parser.add_argument("--force-ocr", action="store_true", help="Forçar OCR mesmo se o PDF tiver texto selecionável")
    parser.add_argument("--poppler", help="Caminho da pasta bin do Poppler (ex.: C:\\tools\\poppler\\bin)")
    parser.add_argument("--tesseract", help="Caminho do executável do Tesseract (ex.: C:\\Program Files\\Tesseract-OCR\\tesseract.exe)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI para rasterização no OCR (padrão: 300)")
    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf)
    if not os.path.isfile(pdf_path):
        print(f"[ERRO] PDF não encontrado: {pdf_path}")
        sys.exit(1)

    out_docx = (
        os.path.abspath(args.output)
        if args.output
        else os.path.splitext(pdf_path)[0] + ".docx"
    )

    # 1) Decide se precisa de OCR
    needs_ocr = args.force_ocr or (not has_selectable_text(pdf_path))

    # 2) Se precisar de OCR, cria um PDF pesquisável temporário; senão usa o original
    pdf_for_docx = pdf_path
    tmp_dir = None

    try:
        if needs_ocr:
            tmp_dir = tempfile.TemporaryDirectory()
            ocr_pdf_path = os.path.join(tmp_dir.name, "ocr_searchable.pdf")
            print("[INFO] Rodando OCR (Tesseract)... isso pode levar alguns minutos em PDFs grandes.")
            ocr_pdf_with_tesseract(
                pdf_path=pdf_path,
                out_pdf_path=ocr_pdf_path,
                lang=args.lang,
                poppler_bin=args.poppler,
                dpi=args.dpi,
                tesseract_cmd=args.tesseract,
            )
            pdf_for_docx = ocr_pdf_path
            print("[INFO] OCR concluído. Convertendo para .docx...")

        # 3) Converte PDF (nativo ou OCR) -> DOCX
        pdf_to_docx(pdf_for_docx, out_docx)
        print(f"[OK] Conversão finalizada: {out_docx}")

    finally:
        if tmp_dir:
            tmp_dir.cleanup()


if __name__ == "__main__":
    main()
