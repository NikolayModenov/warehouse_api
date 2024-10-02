from functools import cache
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


@cache
def get_maker():
    db_user = os.getenv('POSTGRES_USER')
    db_pass = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('POSTGRES_DB')
    sqlalchemy_database_url = (
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    engine = create_engine(sqlalchemy_database_url)
    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    return session_local


def get_db():
    maker = get_maker()
    db = maker()
    try:
        yield db
    finally:
        db.close()
