from pathlib import Path

from app.extraction.pdf_extractor import (
    extract_text_from_pdf,
    is_text_based_pdf,
)

from app.parser.invoice_parser import (
    parse_invoice_text,
)


def main():

    folder = Path(
        "data/raw/batch_1"
    )

    pdf_files = sorted(
        folder.glob("*.pdf")
    )[:5]

    print("=" * 70)
    print("PARSER SAMPLE TEST")
    print("=" * 70)

    print(
        f"Testing {len(pdf_files)} invoices"
    )

    passed = 0
    failed = 0

    for pdf_path in pdf_files:

        print()
        print("-" * 70)
        print(pdf_path.name)
        print("-" * 70)

        try:

            text_based = is_text_based_pdf(
                pdf_path
            )

            if text_based:

                text = extract_text_from_pdf(
                    pdf_path
                )

                method = "PyMuPDF"

            else:

                from app.ocr.ocr_engine import (
                    ocr_pdf,
                )

                text = ocr_pdf(
                    pdf_path
                )

                method = "Tesseract OCR"

            invoice = parse_invoice_text(
                text
            )

            print(
                f"Extraction: {method}"
            )

            print(
                f"Vendor: "
                f"{invoice['vendor']}"
            )

            print(
                f"Invoice: "
                f"{invoice['invoice_number']}"
            )

            print(
                f"Date: "
                f"{invoice['invoice_date']}"
            )

            print(
                f"Items: "
                f"{len(invoice['items'])}"
            )

            print(
                f"Subtotal: "
                f"{invoice['subtotal']}"
            )

            print(
                f"Tax: "
                f"{invoice['tax']}"
            )

            print(
                f"Total: "
                f"{invoice['total']}"
            )

            # Basic parser checks
            required_fields = [
                invoice["vendor"],
                invoice["invoice_number"],
                invoice["invoice_date"],
                invoice["subtotal"],
                invoice["total"],
            ]

            if all(
                value is not None
                for value in required_fields
            ) and len(
                invoice["items"]
            ) > 0:

                print("Parser: PASS")
                passed += 1

            else:

                print("Parser: FAIL")
                failed += 1

        except Exception as error:

            print(
                f"ERROR: {error}"
            )

            failed += 1

    print()
    print("=" * 70)
    print("SAMPLE TEST SUMMARY")
    print("=" * 70)

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
