from datetime import date
from decimal import Decimal

from app.database.crud import create_customer, create_invoice


# Create customer
customer = create_customer(
    name="ABC Technologies",
    email="contact@abc.com",
    phone="9876543210",
    address="Gwalior, Madhya Pradesh",
    gstin="22ABCDE1234F1Z5",
)

print("Customer created")
print("Customer ID:", customer.id)


# Invoice items
items = [
    {
        "description": "Laptop",
        "quantity": 1,
        "unit_price": "50000.00",
    },
    {
        "description": "Wireless Mouse",
        "quantity": 2,
        "unit_price": "1000.00",
    },
    {
        "description": "Keyboard",
        "quantity": 1,
        "unit_price": "2000.00",
    },
]


# Create invoice
invoice = create_invoice(
    invoice_number="INV-1001",
    customer_id=customer.id,
    invoice_date=date.today(),
    items=items,
    tax_rate=Decimal("18"),
)


print("\nInvoice created")
print("----------------------")
print("Invoice ID:", invoice.id)
print("Invoice Number:", invoice.invoice_number)
print("Subtotal:", invoice.subtotal)
print("Tax:", invoice.tax)
print("Total:", invoice.total)
print("Status:", invoice.status)