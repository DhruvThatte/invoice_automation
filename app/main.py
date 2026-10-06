import sys

from app.pipeline import (
    process_invoice,
)


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python main.py <invoice.pdf>"
        )

        sys.exit(1)

    pdf_path = sys.argv[1]

    try:

        result = process_invoice(
            pdf_path
        )

        if result["status"] == "review":

            print(
                "\nInvoice requires manual review."
            )

            sys.exit(2)

        if result["status"] == "duplicate":

            print(
                "\nInvoice already exists "
                "in the database."
            )

            sys.exit(0)

        print(
            "\nInvoice processing completed."
        )

    except Exception as error:

        import traceback

        print(
            f"\nERROR: {error}"
        )

        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()