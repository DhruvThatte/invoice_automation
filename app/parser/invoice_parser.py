import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

def clean_amount(value: str):
    if value is None:
        return None

    value = value.strip()

    value = re.sub(
        r"^[A-Za-z₹$€£]+\s*",
        "",
        value,
    )

    value = value.replace(",", "")

    value = re.sub(
        r"[^\d.-]",
        "",
        value,
    )

    if not value:
        return None

    try:
        return Decimal(value)

    except InvalidOperation:
        return None


def parse_date(value: str):
    """
    Convert common invoice date formats
    into YYYY-MM-DD.
    """

    value = value.strip()

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d.%m.%Y",
    ]

    for date_format in formats:

        try:

            return datetime.strptime(
                value,
                date_format,
            ).strftime("%Y-%m-%d")

        except ValueError:
            continue

    return None


def parse_invoice_text(
    text: str,
) -> dict:
    """
    Parse invoice text from the dataset.

    Supports the invoice format:

        Invoice no:
        Date of issue:
        Seller:
        Tax Id:
        GSTIN:
        ITEMS
        SUMMARY
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    invoice = {
        "vendor": None,
        "invoice_number": None,
        "invoice_date": None,
        "gstin": None,
        "items": [],
        "subtotal": None,
        "tax": None,
        "cgst": None,
        "sgst": None,
        "igst": None,
        "total": None,
    }

    # --------------------------------------------------
    # INVOICE NUMBER
    # --------------------------------------------------

    for i, line in enumerate(lines):

        match = re.search(
            r"Invoice\s*no\s*:\s*(.+)",
            line,
            re.IGNORECASE,
        )

        if match:

            invoice["invoice_number"] = (
                match.group(1).strip()
            )

            break

    # --------------------------------------------------
    # DATE
    # --------------------------------------------------

    for i, line in enumerate(lines):

        if re.search(
            r"Date\s+of\s+issue\s*:",
            line,
            re.IGNORECASE,
        ):

            if i + 1 < len(lines):

                invoice["invoice_date"] = (
                    parse_date(
                        lines[i + 1]
                    )
                )

            break

    # --------------------------------------------------
    # SELLER / VENDOR
    # --------------------------------------------------

    for i, line in enumerate(lines):

        if re.match(
            r"Seller\s*:",
            line,
            re.IGNORECASE,
        ):

            if i + 1 < len(lines):

                invoice["vendor"] = (
                    lines[i + 1]
                )

            break

    # --------------------------------------------------
    # GSTIN
    # --------------------------------------------------

    for line in lines:

        match = re.search(
            r"GSTIN\s*:\s*([A-Z0-9]+)",
            line,
            re.IGNORECASE,
        )

        if match:

            invoice["gstin"] = (
                match.group(1)
            )

            break

    # --------------------------------------------------
    # ITEMS
    # --------------------------------------------------

    try:

        items_start = next(
            i
            for i, line in enumerate(lines)
            if line.upper() == "ITEMS"
        )

    except StopIteration:

        items_start = None

    try:

        summary_start = next(
            i
            for i, line in enumerate(lines)
            if line.upper() == "SUMMARY"
        )

    except StopIteration:

        summary_start = len(lines)

    if items_start is not None:

        item_lines = lines[
            items_start + 1 : summary_start
        ]

        invoice["items"] = parse_items(
            item_lines
        )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    if summary_start < len(lines):

        summary_lines = lines[
            summary_start + 1 :
        ]

        parse_summary(
            summary_lines,
            invoice,
        )

    return invoice


def parse_items(lines: list[str]) -> list[dict]:
    """
    Parse invoice items from the ITEMS section.

    Supports multi-line descriptions.

    Expected structure:

        1.
        Description...
        9.00
        pcs
        74,120.00
        667,080.00
        10%
        733,788.00
    """

    items = []

    i = 0

    while i < len(lines):

        # Find item number
        if not re.fullmatch(r"\d+\.", lines[i]):
            i += 1
            continue

        i += 1

        # ------------------------------------------------
        # Description
        # Continue until we find the quantity.
        # ------------------------------------------------

        description_parts = []

        while i < len(lines):

            if re.fullmatch(
                r"\d+(?:\.\d+)?",
                lines[i].replace(",", ""),
            ):
                break

            description_parts.append(lines[i])
            i += 1

        if i >= len(lines):
            break

        # ------------------------------------------------
        # Quantity
        # ------------------------------------------------

        quantity = parse_number(lines[i])
        i += 1

        if quantity is None:
            continue

        # ------------------------------------------------
        # Unit
        # ------------------------------------------------

        if i >= len(lines):
            break

        unit = lines[i]
        i += 1

        # ------------------------------------------------
        # Net Price
        # ------------------------------------------------

        if i >= len(lines):
            break

        unit_price = clean_amount(lines[i])
        i += 1

        # ------------------------------------------------
        # Net Worth
        # ------------------------------------------------

        if i >= len(lines):
            break

        amount = clean_amount(lines[i])
        i += 1

        # ------------------------------------------------
        # VAT %
        # ------------------------------------------------

        if i >= len(lines):
            break

        vat_rate = lines[i]
        i += 1

        # ------------------------------------------------
        # Gross Worth
        # ------------------------------------------------

        if i >= len(lines):
            break

        gross_amount = clean_amount(lines[i])
        i += 1

        # ------------------------------------------------
        # Create item
        # ------------------------------------------------

        description = " ".join(
            description_parts
        ).strip()

        items.append(
            {
                "description": description,
                "quantity": quantity,
                "unit_price": unit_price,
                "amount": amount,
            }
        )

    return items


def parse_summary(
    lines: list[str],
    invoice: dict,
):
    """
    Parse the invoice SUMMARY section.

    Handles layouts where the labels are listed
    first and the values appear afterward.

    Example:

        VAT %
        Net Worth
        VAT
        Gross Worth
        10%
        1,676,976.00
        167,697.60
        1,844,673.60
    """

    amounts = []

    for line in lines:

        line = line.strip()

        # Ignore VAT percentage
        if "%" in line:
            continue

        # Ignore labels
        if line.lower() in {
            "vat %",
            "net worth",
            "vat",
            "gross worth",
            "total",
            "inr",
        }:
            continue

        amount = clean_amount(line)

        if amount is not None:
            amounts.append(amount)

    # -----------------------------------------------
    # First three monetary values in the summary are:
    #
    # Net Worth
    # VAT
    # Gross Worth
    # -----------------------------------------------

    if len(amounts) >= 3:

        invoice["subtotal"] = amounts[0]

        invoice["tax"] = amounts[1]

        invoice["total"] = amounts[2]

def parse_number(value: str):
    if value is None:
        return None

    value = value.replace(",", "")

    value = re.sub(
        r"[^\d.-]",
        "",
        value,
    )

    if not value:
        return None

    try:
        return Decimal(value)

    except InvalidOperation:
        return None