from pypdf import PdfReader, PdfWriter

ORIGINAL_FILE = r"arquivo.pdf"

writer = PdfWriter(clone_from=ORIGINAL_FILE)

for page in writer.pages:
    for img in page.images:
        img.replace(img.image, quality=10)

with open("out.pdf", "wb") as f:
    writer.write(f)