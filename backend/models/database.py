from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

# Create database engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=Config.DEBUG)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Base class for models
Base = declarative_base()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(engine)

def get_session():
    """Get database session"""
    return Session()

def close_session():
    """Close database session"""
    Session.remove()
