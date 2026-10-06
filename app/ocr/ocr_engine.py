from pathlib import Path

import pymupdf as fitz
import pytesseract

from PIL import Image


def ocr_image(
    image_path: str | Path,
) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = Image.open(image_path)

    text = pytesseract.image_to_string(
        image
    )

    return text


def ocr_pdf(
    pdf_path: str | Path,
) -> str:
    """
    Extract text from a scanned/image-based PDF
    using Tesseract OCR.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "Input file must be a PDF."
        )

    extracted_text = []

    with fitz.open(pdf_path) as document:

        for page_number, page in enumerate(
            document,
            start=1,
        ):

            # Render PDF page as an image.
            pixmap = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            image = Image.frombytes(
                "RGB",
                [
                    pixmap.width,
                    pixmap.height,
                ],
                pixmap.samples,
            )

            text = pytesseract.image_to_string(
                image
            )

            if text.strip():

                extracted_text.append(
                    f"--- Page {page_number} ---\n"
                    f"{text}"
                )

    return "\n\n".join(
        extracted_text
    )