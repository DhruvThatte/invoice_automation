from pathlib import Path

from app.parser.invoice_parser import (
    parse_invoice_text,
)

from app.validation.invoice_validator import (
    validate_invoice,
)


TEXT_PATH = Path(
    "data/processed/INV-1001.txt"
)


def main():

    text = TEXT_PATH.read_text(
        encoding="utf-8"
    )

    invoice = parse_invoice_text(
        text
    )

    result = validate_invoice(
        invoice
    )

    print("=" * 60)
    print("INVOICE VALIDATION")
    print("=" * 60)

    if result["is_valid"]:

        print(
            "VALIDATION PASSED"
        )

        print(
            "Invoice is ready for "
            "database storage."
        )

    else:

        print(
            "VALIDATION FAILED"
        )

        print()

        print("Errors:")

        for error in result["errors"]:
            print(
                f"- {error}"
            )

    print("=" * 60)


if __name__ == "__main__":
    main()
