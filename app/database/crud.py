from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.database.database import engine
from app.database.models import Customer, Invoice, InvoiceItem


def create_customer(
    name: str,
    email: str | None = None,
    phone: str | None = None,
    address: str | None = None,
    gstin: str | None = None,
):
    with Session(engine) as session:

        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            gstin=gstin,
        )

        session.add(customer)
        session.commit()
        session.refresh(customer)

        return customer


def create_invoice(
    invoice_number: str,
    customer_id: int,
    invoice_date: date,
    items: list[dict],
    tax_rate: Decimal,
):
    with Session(engine) as session:

        # Check that customer exists
        customer = session.get(Customer, customer_id)

        if not customer:
            raise ValueError(
                f"Customer with ID {customer_id} does not exist."
            )

        # Calculate subtotal
        subtotal = Decimal("0.00")

        for item in items:
            quantity = Decimal(str(item["quantity"]))
            unit_price = Decimal(str(item["unit_price"]))

            amount = quantity * unit_price
            subtotal += amount

        # Calculate tax
        tax = subtotal * tax_rate / Decimal("100")

        # Calculate total
        total = subtotal + tax

        # Create invoice
        invoice = Invoice(
            invoice_number=invoice_number,
            customer_id=customer_id,
            invoice_date=invoice_date,
            subtotal=subtotal,
            tax=tax,
            total=total,
            status="pending",
        )

        session.add(invoice)
        session.flush()

        # Create invoice items
        for item in items:

            quantity = int(item["quantity"])
            unit_price = Decimal(str(item["unit_price"]))
            amount = Decimal(quantity) * unit_price

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                description=item["description"],
                quantity=quantity,
                unit_price=unit_price,
                amount=amount,
            )

            session.add(invoice_item)

        session.commit()
        session.refresh(invoice)

        return invoice