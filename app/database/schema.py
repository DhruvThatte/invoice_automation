from app.database.connection import (
    get_connection,
)


CREATE_INVOICES_TABLE = """
CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,

    vendor VARCHAR(255) NOT NULL,

    invoice_number VARCHAR(100) NOT NULL,

    invoice_date DATE NOT NULL,

    gstin VARCHAR(15),

    subtotal NUMERIC(12, 2),

    tax NUMERIC(12, 2),

    cgst NUMERIC(12, 2),

    sgst NUMERIC(12, 2),

    igst NUMERIC(12, 2),

    total NUMERIC(12, 2),

    status VARCHAR(20) NOT NULL DEFAULT 'approved',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vendor, invoice_number)
);
"""


CREATE_INVOICE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS invoice_items (
    id BIGSERIAL PRIMARY KEY,

    invoice_id BIGINT NOT NULL,

    description TEXT NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(12, 2) NOT NULL,

    amount NUMERIC(12, 2) NOT NULL,

    FOREIGN KEY (invoice_id)
        REFERENCES invoices(id)
        ON DELETE CASCADE
);
"""


def create_tables():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                CREATE_INVOICES_TABLE
            )

            cursor.execute(
                CREATE_INVOICE_ITEMS_TABLE
            )

        connection.commit()

        print(
            "Database tables created successfully."
        )

    finally:

        connection.close()


if __name__ == "__main__":
    create_tables()
