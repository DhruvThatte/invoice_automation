from pathlib import Path

from app.parser.invoice_parser import (
    parse_invoice_text,
)


TEXT_PATH = Path(
    "data/processed/INV-1001.txt"
)


def main():

    if not TEXT_PATH.exists():
        raise FileNotFoundError(
            f"Text file not found: {TEXT_PATH}"
        )

    text = TEXT_PATH.read_text(
        encoding="utf-8"
    )

    invoice = parse_invoice_text(
        text
    )

    print("=" * 60)
    print("STRUCTURED INVOICE DATA")
    print("=" * 60)

    for key, value in invoice.items():
        print(f"{key}: {value}")

    print("=" * 60)


if __name__ == "__main__":
    main()
