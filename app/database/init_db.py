from app.database.database import engine
from app.database.models import Base


def init_database():
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()
