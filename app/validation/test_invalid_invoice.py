from decimal import Decimal

from app.validation.invoice_validator import (
    validate_invoice,
)


invoice = {
    "vendor": "ABC Technologies",
    "invoice_number": "INV-1001",
    "invoice_date": "2026-10-05",
    "gstin": "22ABCDE1234F1Z5",

    "items": [
        {
            "description": "Laptop",
            "quantity": 1,
            "unit_price": Decimal("50000.00"),
            "amount": Decimal("45000.00"),
        }
    ],

    "subtotal": Decimal("45000.00"),
    "tax": Decimal("9720.00"),
    "total": Decimal("54720.00"),
}


result = validate_invoice(
    invoice
)


print("=" * 60)
print("INVALID INVOICE TEST")
print("=" * 60)

if result["is_valid"]:

    print("VALIDATION PASSED")

else:

    print("VALIDATION FAILED")

    for error in result["errors"]:

        print(
            f"- {error}"
        )

print("=" * 60)
