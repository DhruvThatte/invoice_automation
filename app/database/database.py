import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")


engine = create_engine(
    DATABASE_URL,
    echo=True
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print(result.fetchone())


if __name__ == "__main__":
    test_connection()