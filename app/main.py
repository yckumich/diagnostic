from sqlalchemy.orm import Session
from data.database import engine, Base, get_db
from data.models import *  # Import all models generated in models.py

# Create the database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)

# Function to test the database connection
def test_connection():
    # Create a new session
    db = Session(bind=engine)
    try:
        # Query the first 10 records from a table (adjust the table name as needed)
        # Replace 'YourTableName' with an actual table name from your models
        results = db.query(t_tableau3_t2_tjfs_join_edl_dashadmin).limit(2).all()
        for result in results:
            print()
            print(result)
    finally:
        db.close()

# Test the connection
if __name__ == "__main__":
    test_connection()
