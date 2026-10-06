from pathlib import Path

from app.pipeline import process_invoice

import csv

def save_batch_report(
    results: list[dict],
    output_path: str | Path,
):
    """
    Save batch processing results to CSV.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "file",
                "status",
                "invoice_id",
                "errors",
            ],
        )

        writer.writeheader()

        for result in results:

            writer.writerow(
                {
                    "file": result.get(
                        "file"
                    ),
                    "status": result.get(
                        "status"
                    ),
                    "invoice_id": result.get(
                        "invoice_id"
                    ),
                    "errors": " | ".join(
                        result.get(
                            "errors",
                            [],
                        )
                    ),
                }
            )

    print(
        f"\nBatch report saved to: "
        f"{output_path}"
    )
def process_batch(
    input_directory: str | Path,
) -> dict:

    input_directory = Path(input_directory)

    if not input_directory.exists():
        raise FileNotFoundError(
            f"Directory not found: {input_directory}"
        )

    pdf_files = sorted(
        input_directory.glob("*.pdf")
    )

    if not pdf_files:
        raise ValueError(
            f"No PDF files found in: "
            f"{input_directory}"
        )

    results = []

    approved = 0
    duplicates = 0
    review = 0
    failed = 0

    total = len(pdf_files)

    print("=" * 60)
    print("BATCH INVOICE PROCESSING")
    print("=" * 60)

    print(
        f"\nFound {total} PDF files."
    )

    for index, pdf_path in enumerate(
        pdf_files,
        start=1,):

        print("\n" + "=" * 60)

        print(
            f"[{index}/{total}] "
            f"{pdf_path.name}"
        )

        print("=" * 60)

        try:

            result = process_invoice(
                pdf_path
            )

            status = result.get(
                "status"
            )

            if status == "approved":

                approved += 1

            elif status == "duplicate":

                duplicates += 1

            elif status == "review":

                review += 1

            else:

                failed += 1

            results.append(
                {
                    "file": pdf_path.name,
                    "status": status,
                    "invoice_id": result.get(
                        "invoice_id"
                    ),
                    "errors": result.get(
                        "errors",
                        [],
                    ),
                }
            )
           

        except Exception as error:

            failed += 1

            results.append(
                {
                    "file": pdf_path.name,
                    "status": "failed",
                    "invoice_id": None,
                    "errors": [
                        str(error)
                    ],
                }
            )

            print(
                f"\nERROR: {error}"
            )

            # Important:
            # Continue processing the
            # remaining invoices.

            continue
        # --------------------------------------------------
    # REVIEW REPORT
    # --------------------------------------------------

    review_results = [
        result
        for result in results
        if result["status"] == "review"
    ]

    if review_results:

        print("\n")
        print("=" * 60)
        print("REVIEW REQUIRED")
        print("=" * 60)

        for result in review_results:

            print(
                f"\n{result['file']}"
            )

            for error in result["errors"]:

                print(
                    f"  - {error}"
                )

        print("=" * 60)

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    print("\n")
    print("=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)

    print(
        f"Total:       {total}"
    )

    print(
        f"Approved:    {approved}"
    )

    print(
        f"Duplicates:  {duplicates}"
    )

    print(
        f"Review:      {review}"
    )

    print(
        f"Failed:      {failed}"
    )

    print("=" * 60)
    save_batch_report(
    results,
    "data/reports/batch_report.csv",
)

    return {
        "total": total,
        "approved": approved,
        "duplicates": duplicates,
        "review": review,
        "failed": failed,
        "results": results,
    }
