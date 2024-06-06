from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .logging import logger
from ..paths import DATABASE_URI

engine = create_engine(DATABASE_URI)
session = sessionmaker(bind=engine)
Base = declarative_base()
logger.debug("Initialized database.")

def teardown_database():
    engine.dispose()
    logger.debug("Database teardown complete.")
