from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_invoice_pdf(invoice, output_path):
    """
    Generate a PDF invoice from an SQLAlchemy Invoice object.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        "InvoiceNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
    )

    elements = []

    # -----------------------------
    # Header
    # -----------------------------

    elements.append(
        Paragraph("INVOICE", title_style)
    )

    elements.append(
        Paragraph(
            f"<b>Invoice Number:</b> {invoice.invoice_number}",
            normal_style,
        )
    )

    elements.append(
        Paragraph(
            f"<b>Invoice Date:</b> {invoice.invoice_date}",
            normal_style,
        )
    )

    elements.append(Spacer(1, 10))

    # -----------------------------
    # Customer Information
    # -----------------------------

    customer = invoice.customer

    customer_data = [
        [
            Paragraph("<b>Bill To</b>", normal_style),
            Paragraph("<b>Customer Details</b>", normal_style),
        ],
        [
            Paragraph(customer.name, normal_style),
            Paragraph(
                f"Email: {customer.email or '-'}<br/>"
                f"Phone: {customer.phone or '-'}<br/>"
                f"GSTIN: {customer.gstin or '-'}<br/>"
                f"Address: {customer.address or '-'}",
                normal_style,
            ),
        ],
    ]

    customer_table = Table(
        customer_data,
        colWidths=[80 * mm, 80 * mm],
    )

    customer_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(customer_table)

    elements.append(Spacer(1, 15))

    # -----------------------------
    # Invoice Items
    # -----------------------------

    item_data = [
        [
            Paragraph("<b>Description</b>", normal_style),
            Paragraph("<b>Quantity</b>", normal_style),
            Paragraph("<b>Unit Price</b>", normal_style),
            Paragraph("<b>Amount</b>", normal_style),
        ]
    ]

    for item in invoice.items:
        item_data.append(
            [
                Paragraph(item.description, normal_style),
                Paragraph(str(item.quantity), normal_style),
                Paragraph(f"₹{item.unit_price:.2f}", normal_style),
                Paragraph(f"₹{item.amount:.2f}", normal_style),
            ]
        )

    item_table = Table(
        item_data,
        colWidths=[75 * mm, 25 * mm, 35 * mm, 35 * mm],
        repeatRows=1,
    )

    item_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(item_table)

    elements.append(Spacer(1, 15))

    # -----------------------------
    # Totals
    # -----------------------------

    totals_data = [
        [
            Paragraph("<b>Subtotal</b>", normal_style),
            Paragraph(f"₹{invoice.subtotal:.2f}", normal_style),
        ],
        [
            Paragraph("<b>Tax / GST</b>", normal_style),
            Paragraph(f"₹{invoice.tax:.2f}", normal_style),
        ],
        [
            Paragraph("<b>Grand Total</b>", normal_style),
            Paragraph(f"<b>₹{invoice.total:.2f}</b>", normal_style),
        ],
    ]

    totals_table = Table(
        totals_data,
        colWidths=[45 * mm, 45 * mm],
        hAlign="RIGHT",
    )

    totals_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(totals_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"<b>Status:</b> {invoice.status}",
            normal_style,
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Thank you for your business.",
            normal_style,
        )
    )

    # Build PDF
    document.build(elements)

    return output_path
