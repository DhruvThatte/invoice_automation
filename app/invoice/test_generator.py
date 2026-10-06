from pathlib import Path

from sqlalchemy.orm import Session

from app.database.database import engine
from app.database.models import Invoice
from app.invoice.generator import generate_invoice_pdf


OUTPUT_DIR = Path("data/processed")


with Session(engine) as session:

    invoice = session.query(Invoice).first()

    if not invoice:
        raise ValueError(
            "No invoice found in the database."
        )

    output_path = (
        OUTPUT_DIR
        / f"{invoice.invoice_number}.pdf"
    )

    generate_invoice_pdf(
        invoice,
        output_path,
    )

    print("Invoice PDF generated:")
    print(output_path)