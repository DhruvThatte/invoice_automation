from app.database.connection import (
    get_connection,
)


def find_invoice(
    vendor: str,
    invoice_number: str,
):
    """
    Find an existing invoice using
    vendor + invoice number.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM invoices
                WHERE vendor = %s
                  AND invoice_number = %s;
                """,
                (
                    vendor,
                    invoice_number,
                ),
            )

            row = cursor.fetchone()

            if row:
                return row[0]

            return None

    finally:

        connection.close()


def insert_invoice(
    invoice: dict,
) -> int:
    """
    Insert an invoice and its items.

    Returns the generated invoice ID.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO invoices (
                    vendor,
                    invoice_number,
                    invoice_date,
                    gstin,
                    subtotal,
                    tax,
                    cgst,
                    sgst,
                    igst,
                    total,
                    status
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s
                )
                RETURNING id;
                """,
                (
                    invoice["vendor"],
                    invoice["invoice_number"],
                    invoice["invoice_date"],
                    invoice["gstin"],
                    invoice["subtotal"],
                    invoice["tax"],
                    invoice["cgst"],
                    invoice["sgst"],
                    invoice["igst"],
                    invoice["total"],
                    "approved",
                ),
            )

            invoice_id = cursor.fetchone()[0]

            for item in invoice["items"]:

                cursor.execute(
                    """
                    INSERT INTO invoice_items (
                        invoice_id,
                        description,
                        quantity,
                        unit_price,
                        amount
                    )
                    VALUES (
                        %s, %s, %s, %s, %s
                    );
                    """,
                    (
                        invoice_id,
                        item["description"],
                        item["quantity"],
                        item["unit_price"],
                        item["amount"],
                    ),
                )

        connection.commit()

        return invoice_id

    finally:

        connection.close()