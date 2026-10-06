import sys
from pathlib import Path

from app.pipeline import process_invoice


def process_single_invoice(pdf_path: Path):
    """
    Process one invoice.
    """

    try:

        result = process_invoice(pdf_path)

        return result

    except Exception as error:

        print(
            f"\nERROR processing {pdf_path.name}: "
            f"{error}"
        )

        return {
            "success": False,
            "status": "failed",
            "error": str(error),
        }


def process_batch(folder_path: Path):
    """
    Process every PDF inside a directory.
    """

    if not folder_path.exists():

        print(
            f"ERROR: Folder not found: "
            f"{folder_path}"
        )

        sys.exit(1)

    if not folder_path.is_dir():

        print(
            f"ERROR: Not a directory: "
            f"{folder_path}"
        )

        sys.exit(1)

    pdf_files = sorted(
        folder_path.glob("*.pdf")
    )

    if not pdf_files:

        print(
            f"No PDF files found in "
            f"{folder_path}"
        )

        sys.exit(1)

    print()
    print("=" * 60)
    print("BATCH INVOICE PROCESSING")
    print("=" * 60)

    print(
        f"Input folder: {folder_path}"
    )

    print(
        f"PDF files found: {len(pdf_files)}"
    )

    print("=" * 60)

    approved = 0
    duplicate = 0
    review = 0
    failed = 0

    for index, pdf_path in enumerate(
        pdf_files,
        start=1,
    ):

        print()
        print(
            f"[{index}/{len(pdf_files)}] "
            f"{pdf_path.name}"
        )

        result = process_single_invoice(
            pdf_path
        )

        status = result.get(
            "status"
        )

        if status == "approved":

            approved += 1

        elif status == "duplicate":

            duplicate += 1

        elif status == "review":

            review += 1

        else:

            failed += 1

    print()
    print("=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)

    print(
        f"Total:       {len(pdf_files)}"
    )

    print(
        f"Approved:    {approved}"
    )

    print(
        f"Duplicates:  {duplicate}"
    )

    print(
        f"Review:      {review}"
    )

    print(
        f"Failed:      {failed}"
    )

    print("=" * 60)


def main():

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "  Single invoice:"
        )

        print(
            "    python main.py <invoice.pdf>"
        )

        print()

        print(
            "  Batch processing:"
        )

        print(
            "    python main.py --batch <folder>"
        )

        sys.exit(1)

    # ---------------------------------------------
    # BATCH MODE
    # ---------------------------------------------

    if sys.argv[1] == "--batch":

        if len(sys.argv) != 3:

            print(
                "Usage:"
            )

            print(
                "  python main.py "
                "--batch <folder>"
            )

            sys.exit(1)

        folder_path = Path(
            sys.argv[2]
        )

        process_batch(
            folder_path
        )

        return

    # ---------------------------------------------
    # SINGLE FILE MODE
    # ---------------------------------------------

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "  python main.py <invoice.pdf>"
        )

        print(
            "  python main.py "
            "--batch <folder>"
        )

        sys.exit(1)

    pdf_path = Path(
        sys.argv[1]
    )

    if not pdf_path.exists():

        print(
            f"ERROR: PDF not found: "
            f"{pdf_path}"
        )

        sys.exit(1)

    result = process_single_invoice(
        pdf_path
    )

    if result.get("status") == "review":

        sys.exit(2)

    if result.get("status") == "failed":

        sys.exit(1)


if __name__ == "__main__":
    main()