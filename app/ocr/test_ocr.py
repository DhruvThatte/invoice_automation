import sys

from app.ocr.ocr_engine import (
    ocr_image,
    ocr_pdf,
)


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python -m app.ocr.test_ocr <file>"
        )

        sys.exit(1)

    file_path = sys.argv[1]

    if file_path.lower().endswith(
        ".pdf"
    ):

        text = ocr_pdf(
            file_path
        )

    else:

        text = ocr_image(
            file_path
        )

    print("=" * 60)
    print("OCR RESULT")
    print("=" * 60)

    print(text)

    print("=" * 60)


if __name__ == "__main__":
    main()