from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URI = settings.database_url.get_secret_value()

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
    # connect_args={"check_same_thread" : False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db


