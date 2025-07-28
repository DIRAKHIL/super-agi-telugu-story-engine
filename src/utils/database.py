"""
Database utilities for the AI Emotional Engine for Telugu Story Creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

Base = declarative_base()


def init_db(config):
    """
    Initialize the database.
    
    Args:
        config (dict): Configuration dictionary.
    
    Returns:
        tuple: Engine and session maker.
    """
    db_url = config["database"]["url"]
    echo = config["database"]["echo"]
    
    logger.info(f"Initializing database with URL: {db_url}")
    
    engine = create_engine(db_url, echo=echo)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database initialization complete")
    
    return engine, SessionLocal


def get_db(SessionLocal):
    """
    Get database session.
    
    Args:
        SessionLocal: Session maker.
    
    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()