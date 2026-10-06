from app.database.connection import (
    get_connection,
)


def main():

    connection = get_connection()

    try:

        print(
            "PostgreSQL connection successful!"
        )

    finally:

        connection.close()


if __name__ == "__main__":
    main()
