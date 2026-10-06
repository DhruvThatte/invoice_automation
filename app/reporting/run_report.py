from app.reporting.invoice_report import (
    get_invoice_summary,
    get_vendor_summary,
    get_yearly_summary,
)


def main():

    print("=" * 60)
    print("INVOICE DATABASE REPORT")
    print("=" * 60)

    # --------------------------------------------------
    # OVERALL SUMMARY
    # --------------------------------------------------

    summary = get_invoice_summary()

    (
        total_invoices,
        total_subtotal,
        total_tax,
        total_value,
        average_invoice_value,
    ) = summary

    print("\nOVERALL SUMMARY")
    print("-" * 60)

    print(
        f"Total invoices:        {total_invoices}"
    )

    print(
        f"Total subtotal:        {total_subtotal}"
    )

    print(
        f"Total tax:             {total_tax}"
    )

    print(
        f"Total invoice value:   {total_value}"
    )

    print(
        f"Average invoice value: {average_invoice_value}"
    )

    # --------------------------------------------------
    # VENDOR SUMMARY
    # --------------------------------------------------

    print("\nVENDOR SUMMARY")
    print("-" * 60)

    vendors = get_vendor_summary()

    for row in vendors:

        (
            vendor,
            invoice_count,
            subtotal,
            tax,
            total,
        ) = row

        print(
            f"{vendor}"
        )

        print(
            f"  Invoices: {invoice_count}"
        )

        print(
            f"  Subtotal: {subtotal}"
        )

        print(
            f"  Tax:      {tax}"
        )

        print(
            f"  Total:    {total}"
        )

    # --------------------------------------------------
    # YEARLY SUMMARY
    # --------------------------------------------------

    print("\nYEARLY SUMMARY")
    print("-" * 60)

    yearly = get_yearly_summary()

    for row in yearly:

        (
            year,
            invoice_count,
            total_value,
        ) = row

        print(
            f"{int(year)}"
            f" → {invoice_count} invoices"
            f" → {total_value}"
        )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
