from decimal import Decimal

from app.database.connection import get_connection


def get_invoice_summary():
    """
    Return overall invoice statistics.
    """

    query = """
        SELECT
            COUNT(*) AS total_invoices,
            COALESCE(SUM(subtotal), 0) AS total_subtotal,
            COALESCE(SUM(tax), 0) AS total_tax,
            COALESCE(SUM(total), 0) AS total_value,
            COALESCE(AVG(total), 0) AS average_invoice_value
        FROM invoices;
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchone()


def get_vendor_summary():
    """
    Return invoice statistics grouped by vendor.
    """

    query = """
        SELECT
            vendor,
            COUNT(*) AS invoice_count,
            COALESCE(SUM(subtotal), 0) AS subtotal,
            COALESCE(SUM(tax), 0) AS tax,
            COALESCE(SUM(total), 0) AS total
        FROM invoices
        GROUP BY vendor
        ORDER BY total DESC;
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchall()


def get_yearly_summary():
    """
    Return invoice statistics grouped by year.
    """

    query = """
        SELECT
            EXTRACT(
                YEAR FROM invoice_date
            ) AS year,

            COUNT(*) AS invoice_count,

            COALESCE(
                SUM(total),
                0
            ) AS total_value

        FROM invoices

        WHERE invoice_date IS NOT NULL

        GROUP BY year

        ORDER BY year;
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchall()
