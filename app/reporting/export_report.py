from pathlib import Path

import pandas as pd


def export_report(
    results: list[dict],
    output_directory: str | Path = "data/reports",
) -> tuple[Path, Path]:
    """
    Export invoice processing results to CSV and Excel.
    """

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        output_directory
        / "invoice_report.csv"
    )

    excel_path = (
        output_directory
        / "invoice_report.xlsx"
    )

    # Convert results into a DataFrame.
    dataframe = pd.DataFrame(results)

    # Rename columns for the final report.
    dataframe = dataframe.rename(
        columns={
            "file_name": "File Name",
            "invoice_number": "Invoice Number",
            "vendor": "Vendor",
            "invoice_date": "Invoice Date",
            "gstin": "GSTIN",
            "items": "Items",
            "subtotal": "Subtotal",
            "tax": "Tax",
            "total": "Total",
            "status": "Status",
        }
    )

    # Keep the report columns in a predictable order.
    columns = [
        "File Name",
        "Invoice Number",
        "Vendor",
        "Invoice Date",
        "GSTIN",
        "Items",
        "Subtotal",
        "Tax",
        "Total",
        "Status",
    ]

    dataframe = dataframe[
        columns
    ]

    # CSV
    dataframe.to_csv(
        csv_path,
        index=False,
    )

    # Excel
    with pd.ExcelWriter(
        excel_path,
        engine="openpyxl",
    ) as writer:

        dataframe.to_excel(
            writer,
            sheet_name="Invoices",
            index=False,
        )

        worksheet = (
            writer.sheets["Invoices"]
        )

        # Freeze header row.
        worksheet.freeze_panes = "A2"

        # Add filters.
        worksheet.auto_filter.ref = (
            worksheet.dimensions
        )

        # Set useful column widths.
        widths = {
            "A": 30,
            "B": 18,
            "C": 35,
            "D": 15,
            "E": 20,
            "F": 10,
            "G": 18,
            "H": 18,
            "I": 18,
            "J": 15,
        }

        for column, width in widths.items():

            worksheet.column_dimensions[
                column
            ].width = width

    return csv_path, excel_path