from app.ocr.pdf_to_image import (
    convert_pdf_to_images,
)


PDF_PATH = "data/processed/INV-1001.pdf"

OUTPUT_DIR = "data/processed/ocr_images"


images = convert_pdf_to_images(
    PDF_PATH,
    OUTPUT_DIR,
)


print("Generated images:")

for image in images:
    print(image)