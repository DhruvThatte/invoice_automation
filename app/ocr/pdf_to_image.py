from pathlib import Path

import pymupdf as fitz


def convert_pdf_to_images(
    pdf_path: str | Path,
    output_dir: str | Path,
):
    """
    Convert every PDF page into a PNG image.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_images = []

    with fitz.open(pdf_path) as document:

        for page_number, page in enumerate(
            document,
            start=1,
        ):

            # Render page at higher resolution.
            matrix = fitz.Matrix(2, 2)

            pixmap = page.get_pixmap(
                matrix=matrix
            )

            output_path = (
                output_dir
                / f"page_{page_number}.png"
            )

            pixmap.save(
                str(output_path)
            )

            generated_images.append(
                output_path
            )

    return generated_images