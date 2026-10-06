from app.extraction.pdf_extractor import (
    extract_text_from_pdf,
    save_extracted_text,
    is_text_based_pdf,
)


PDF_PATH = "data/processed/INV-1001.pdf"
OUTPUT_PATH = "data/processed/INV-1001.txt"


if is_text_based_pdf(PDF_PATH):

    print("Digital/text PDF detected.")

    text = extract_text_from_pdf(PDF_PATH)

    save_extracted_text(
        text,
        OUTPUT_PATH,
    )

    print(
        f"Extracted text saved to: {OUTPUT_PATH}"
    )

else:

    print(
        "Scanned/image PDF detected."
    )

    print(
        "OCR will be used in the next stage."
    )