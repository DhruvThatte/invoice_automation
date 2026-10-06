from pathlib import Path

from app.ocr.ocr_engine import (
    ocr_pdf,
)

from app.extraction.pdf_extractor import (
    extract_text_from_pdf,
    is_text_based_pdf,
)

from app.parser.invoice_parser import (
    parse_invoice_text,
)

from app.validation.invoice_validator import (
    validate_invoice,
)

from app.database.invoice_repository import (
    insert_invoice,
    find_invoice,
)


def process_invoice(
    pdf_path: str | Path,
) -> dict:
    """
    Process an invoice from PDF to PostgreSQL.

    Pipeline:

        PDF
         ↓
        Text extraction
         ↓
        Parsing
         ↓
        Validation
         ↓
        PostgreSQL
    """

    pdf_path = Path(pdf_path)

    print("=" * 60)
    print("INVOICE AUTOMATION")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1 — CHECK FILE
    # --------------------------------------------------

    print("\n[1/4] Checking PDF...")

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":

        raise ValueError(
            "Input file must be a PDF."
        )

    print(
        f"Input: {pdf_path}"
    )

    # --------------------------------------------------
    # STEP 2 — EXTRACT TEXT
    # --------------------------------------------------

    print(
    "\n[2/4] Extracting invoice text..."
)

    text_based = is_text_based_pdf(
        pdf_path
    )

    if text_based:

        print(
            "PDF type: Digital/Text PDF"
        )

        text = extract_text_from_pdf(
            pdf_path
        )

    else:

        print(
            "PDF type: Scanned/Image PDF"
        )

        print(
            "Starting OCR..."
        )

        text = ocr_pdf(
            pdf_path
        )

    if not text.strip():

        raise ValueError(
            "No text could be extracted "
            "from the invoice."
        )

    print(
        "Text extraction successful."
    )
    # --------------------------------------------------
    # STEP 3 — PARSE + VALIDATE
    # --------------------------------------------------

    print(
        "\n[3/4] Parsing invoice..."
    )

    invoice = parse_invoice_text(
        text
    )

    print(
        f"Vendor: "
        f"{invoice['vendor']}"
    )

    print(
        f"Invoice Number: "
        f"{invoice['invoice_number']}"
    )

    print(
        f"Invoice Date: "
        f"{invoice['invoice_date']}"
    )

    print(
        f"GSTIN: "
        f"{invoice['gstin']}"
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

    print(
        "\nRunning validation..."
    )

    validation = validate_invoice(
        invoice
    )

    if not validation["is_valid"]:

        print(
            "\nVALIDATION FAILED"
        )

        for error in validation["errors"]:

            print(
                f"  - {error}"
            )

        return {
            "success": False,
            "status": "review",
            "errors": validation["errors"],
            "invoice": invoice,
        }

    print(
        "Validation PASSED."
    )

    # --------------------------------------------------
    # STEP 4 — DATABASE
    # --------------------------------------------------

    print(
    "\n[4/4] Saving to PostgreSQL...")

    existing_invoice_id = find_invoice(
        invoice["vendor"],
        invoice["invoice_number"],
    )

    if existing_invoice_id is not None:

        print(
            "\nDUPLICATE INVOICE DETECTED"
        )

        print(
            f"Vendor: {invoice['vendor']}"
        )

        print(
            f"Invoice Number: "
            f"{invoice['invoice_number']}"
        )

        print(
            f"Existing Database ID: "
            f"{existing_invoice_id}"
        )

        print(
            "Invoice was not inserted again."
        )

        print("=" * 60)

        return {
            "success": True,
            "status": "duplicate",
            "invoice_id": existing_invoice_id,
            "invoice": invoice,
        }


    invoice_id = insert_invoice(
        invoice
    )

    print(
        "Invoice saved successfully."
    )

    print(
        f"Database ID: {invoice_id}"
    )

    print("=" * 60)

    return {
        "success": True,
        "status": "approved",
        "invoice_id": invoice_id,
        "invoice": invoice,
    }