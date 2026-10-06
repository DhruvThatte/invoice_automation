from pathlib import Path
import shutil
import sys

from app.pipeline import process_invoice

from app.reporting.export_report import (
    export_report,
)
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
}


def find_invoice_files(
    input_directory: Path,
) -> list[Path]:
    """
    Find supported invoice files in the input directory.
    """

    if not input_directory.exists():
        raise FileNotFoundError(
            f"Input directory not found: {input_directory}"
        )

    if not input_directory.is_dir():
        raise ValueError(
            f"Input path is not a directory: "
            f"{input_directory}"
        )

    files = []

    for file in sorted(input_directory.iterdir()):

        if not file.is_file():
            continue

        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(file)

    return files


def move_file(
    file_path: Path,
    destination_directory: Path,
):
    """
    Move a processed file to its destination directory.
    """

    destination_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        destination_directory
        / file_path.name
    )

    # Avoid overwriting an existing file.
    if destination.exists():

        counter = 1

        while True:

            new_name = (
                f"{file_path.stem}"
                f"_{counter}"
                f"{file_path.suffix}"
            )

            destination = (
                destination_directory
                / new_name
            )

            if not destination.exists():
                break

            counter += 1

    shutil.move(
        str(file_path),
        str(destination),
    )


def process_batch(
    input_directory: str | Path,
) -> list[dict]:

    input_directory = Path(
        input_directory
    )

    project_root = Path(__file__).resolve().parent

    processed_directory = (
        project_root / "data" / "processed"
    )

    review_directory = (
        project_root / "data" / "review"
    )

    failed_directory = (
        project_root / "data" / "failed"
    )

    files = find_invoice_files(
        input_directory
    )

    results = []

    print("=" * 60)
    print("INVOICE AUTOMATION")
    print("=" * 60)

    print(
        f"\nInput directory: "
        f"{input_directory}"
    )

    print(
        f"Files found: {len(files)}"
    )

    if not files:

        print(
            "\nNo invoice files found."
        )

        return results

    # --------------------------------------------------
    # PROCESS EACH FILE
    # --------------------------------------------------

    for index, file_path in enumerate(
        files,
        start=1,
    ):

        print("\n" + "-" * 60)

        print(
            f"[{index}/{len(files)}] "
            f"{file_path.name}"
        )

        try:

            # Your existing pipeline.
            result = process_invoice(
                file_path
            )

            status = result.get(
                "status",
                "failed",
            )

            invoice = result.get(
                "invoice",
                {},
            )

            # --------------------------------------------------
            # APPROVED
            # --------------------------------------------------

            if status == "approved":

                move_file(
                    file_path,
                    processed_directory,
                )

            # --------------------------------------------------
            # DUPLICATE
            # --------------------------------------------------

            elif status == "duplicate":

                # A duplicate has already been
                # successfully stored, so we
                # consider it processed.
                move_file(
                    file_path,
                    processed_directory,
                )

            # --------------------------------------------------
            # REVIEW
            # --------------------------------------------------

            elif status == "review":

                move_file(
                    file_path,
                    review_directory,
                )

            # --------------------------------------------------
            # UNKNOWN STATUS
            # --------------------------------------------------

            else:

                move_file(
                    file_path,
                    failed_directory,
                )

                status = "failed"

            results.append(
                {
                    "file_name": file_path.name,
                    "status": status,
                    "invoice_number": invoice.get(
                        "invoice_number"
                    ),
                    "vendor": invoice.get(
                        "vendor"
                    ),
                    "invoice_date": invoice.get(
                        "invoice_date"
                    ),
                    "gstin": invoice.get(
                        "gstin"
                    ),
                    "subtotal": invoice.get(
                        "subtotal"
                    ),
                    "tax": invoice.get(
                        "tax"
                    ),
                    "total": invoice.get(
                        "total"
                    ),
                    "items": len(
                        invoice.get(
                            "items",
                            [],
                        )
                    ),
                }
            )

        except Exception as error:

            print(
                f"\nERROR processing "
                f"{file_path.name}: {error}"
            )

            try:

                move_file(
                    file_path,
                    failed_directory,
                )

            except Exception as move_error:

                print(
                    f"Could not move file: "
                    f"{move_error}"
                )

            results.append(
                {
                    "file_name": file_path.name,
                    "status": "failed",
                    "invoice_number": None,
                    "vendor": None,
                    "invoice_date": None,
                    "gstin": None,
                    "subtotal": None,
                    "tax": None,
                    "total": None,
                    "items": 0,
                }
            )

    return results


def print_summary(
    results: list[dict],
):

    approved = sum(
        1
        for result in results
        if result["status"] == "approved"
    )

    duplicates = sum(
        1
        for result in results
        if result["status"] == "duplicate"
    )

    review = sum(
        1
        for result in results
        if result["status"] == "review"
    )

    failed = sum(
        1
        for result in results
        if result["status"] == "failed"
    )

    print("\n")
    print("=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)

    print(
        f"Files scanned:       {len(results)}"
    )

    print(
        f"New invoices:        {approved}"
    )

    print(
        f"Already processed:   {duplicates}"
    )

    print(
        f"Review required:     {review}"
    )

    print(
        f"Failed:              {failed}"
    )

    print("=" * 60)


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python automate.py <input_directory>"
        )

        sys.exit(1)

    input_directory = sys.argv[1]

    try:

        results = process_batch(
            input_directory
        )

        print_summary(
            results
        )

        # --------------------------------------------------
        # GENERATE REPORTS
        # --------------------------------------------------

        print(
            "\nGenerating reports..."
        )

        csv_path, excel_path = export_report(
            results
        )

        print(
            f"CSV report:   {csv_path}"
        )

        print(
            f"Excel report: {excel_path}"
        )

    except Exception as error:

        print(
            f"\nERROR: {error}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()

