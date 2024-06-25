from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import generated models
from .models import *

# Database connection parameters
user_name = 'postgres'
password = '172733zZ'
host_name = 'localhost'
port_num = 5432
db_name = 'EDL'

SQLALCHEMY_DATABASE_URL = f"postgresql://{user_name}:{password}@{host_name}/{db_name}"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,       # Increase pool size
    max_overflow=20,    # Allow additional connections beyond the pool size
    pool_timeout=30,    # Wait time before giving up on getting a connection
)
# Create a sessionmaker factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()