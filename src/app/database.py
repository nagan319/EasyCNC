"""
Author: nagan319
Date: 2024/05/31
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from .logging import logger
from ..paths import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return Session()

def close_session():
    Session.remove()

def teardown_db():
    engine.dispose()
    logger.debug("Database teardown complete.")
