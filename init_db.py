import os

from sqlalchemy import MetaData, create_engine

from hw.db import users


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(
        users.insert(),
        [
            {"first_name": "Padmé", "last_name": "Amidala"},
            {"first_name": "Darth", "last_name": "Maul"},
            {"first_name": "Jar Jar", "last_name": "Binks"},
        ],
    )
    conn.close()


if __name__ == "__main__":
    db_url = os.getenv("DATABASE")
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
