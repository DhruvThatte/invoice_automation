import sys

from app.batch.batch_processor import (
    process_batch,
)


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python -m app.batch.run_batch "
            "<directory>"
        )

        sys.exit(1)

    input_directory = sys.argv[1]

    try:

        process_batch(
            input_directory
        )

    except Exception as error:

        print(
            f"\nERROR: {error}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
