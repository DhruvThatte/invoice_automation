from decimal import Decimal


def validate_invoice(invoice: dict) -> dict:
    """
    Validate an extracted invoice.

    Returns:

        {
            "is_valid": True/False,
            "errors": [...]
        }
    """

    errors = []

    # --------------------------------------------------
    # Required fields
    # --------------------------------------------------

    required_fields = {
        "vendor": invoice.get("vendor"),
        "invoice_number": invoice.get("invoice_number"),
        "invoice_date": invoice.get("invoice_date"),
        "subtotal": invoice.get("subtotal"),
        "total": invoice.get("total"),
    }

    for field, value in required_fields.items():

        if value is None or value == "":
            errors.append(
                f"Missing required field: {field}"
            )

    # --------------------------------------------------
    # Items
    # --------------------------------------------------

    items = invoice.get("items", [])

    if not isinstance(items, list):

        errors.append(
            "Invalid items structure"
        )

        return {
            "is_valid": False,
            "errors": errors,
        }

    if not items:

        errors.append(
            "Invoice contains no line items"
        )

    # --------------------------------------------------
    # Validate individual items
    # --------------------------------------------------

    item_total = Decimal("0")

    for index, item in enumerate(
        items,
        start=1,
    ):

        if not isinstance(item, dict):

            errors.append(
                f"Item {index}: invalid item structure"
            )

            continue

        quantity = item.get(
            "quantity"
        )

        unit_price = item.get(
            "unit_price"
        )

        amount = item.get(
            "amount"
        )

        # ----------------------------------------------
        # Required item fields
        # ----------------------------------------------

        if quantity is None:

            errors.append(
                f"Item {index}: missing quantity"
            )

        if unit_price is None:

            errors.append(
                f"Item {index}: missing unit price"
            )

        if amount is None:

            errors.append(
                f"Item {index}: missing amount"
            )

        # ----------------------------------------------
        # Item calculation
        # ----------------------------------------------

        if (
            quantity is not None
            and unit_price is not None
            and amount is not None
        ):

            expected_amount = (
                quantity * unit_price
            )

            difference = abs(
                expected_amount - amount
            )

            if difference > Decimal("0.10"):

                errors.append(
                    f"Item {index}: amount mismatch "
                    f"(expected {expected_amount}, "
                    f"got {amount})"
                )

            item_total += amount

    # --------------------------------------------------
    # Subtotal validation
    # --------------------------------------------------

    subtotal = invoice.get(
        "subtotal"
    )

    if (
        subtotal is not None
        and items
    ):

        difference = abs(
            item_total - subtotal
        )

        if difference > Decimal("0.10"):

            errors.append(
                "Subtotal mismatch: "
                f"items total = {item_total}, "
                f"subtotal = {subtotal}"
            )

    # --------------------------------------------------
    # Total validation
    # --------------------------------------------------

    tax = invoice.get(
        "tax"
    )

    total = invoice.get(
        "total"
    )

    if (
        subtotal is not None
        and tax is not None
        and total is not None
    ):

        calculated_total = (
            subtotal + tax
        )

        difference = abs(
            calculated_total - total
        )

        if difference > Decimal("0.10"):

            errors.append(
                "Total mismatch: "
                f"subtotal + tax = "
                f"{calculated_total}, "
                f"total = {total}"
            )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }