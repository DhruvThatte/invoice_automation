from pathlib import Path

import pymupdf as fitz


def extract_text_from_pdf(
    pdf_path: str | Path,
) -> str:
    """
    Extract selectable text from a PDF.
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

            text = page.get_text()

            if text.strip():

                extracted_text.append(
                    f"--- Page {page_number} ---\n"
                    f"{text}"
                )

    return "\n\n".join(
        extracted_text
    )


def is_text_based_pdf(
    pdf_path: str | Path,
) -> bool:
    """
    Determine whether a PDF contains
    selectable text.
    """

    text = extract_text_from_pdf(
        pdf_path
    )

    return bool(
        text.strip()
    )


def save_extracted_text(
    text: str,
    output_path: str | Path,
):
    """
    Save extracted text to a text file.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        text,
        encoding="utf-8",
    )

    return output_path