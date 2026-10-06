from pathlib import Path

from app.parser.invoice_parser import (
    parse_invoice_text,
)

from app.validation.invoice_validator import (
    validate_invoice,
)

from app.database.invoice_repository import (
    insert_invoice,
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

    validation = validate_invoice(
        invoice
    )

    if not validation["is_valid"]:

        print(
            "Invoice failed validation."
        )

        for error in validation["errors"]:
            print(
                f"- {error}"
            )

        return

    invoice_id = insert_invoice(
        invoice
    )

    print(
        f"Invoice inserted successfully."
    )

    print(
        f"Database ID: {invoice_id}"
    )


if __name__ == "__main__":
    main()