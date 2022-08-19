""" Module handling the SQLalchemy database connection and session setup """

# Imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Database metadata
DATABASE_USERNAME = settings.database_username
DATABASE_SERVER = settings.database_server
DATABASE_PASSWORD = settings.database_password
DATABASE_HOSTNAME = settings.database_hostname
DATABASE_NAME = settings.database_name

# Database connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}"

# Database Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> any:
    """ Gets database session """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()