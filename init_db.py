"""
Initialize the TerminusDB Equipment Database

This script:
1. Connects to TerminusDB
2. Creates the database
3. Sets up the schema
"""

from terminusdb_client import Client
from schema import (
    EquipmentType, EquipmentCondition, Manufacturer, Equipment,
    Tractor, Combine, ConstructionEquipment
)


# Database configuration
DB_NAME = "equipment_db"
DB_LABEL = "Equipment Database"
DB_DESCRIPTION = "A database for tracking tractors, combines, and construction equipment"

# TerminusDB connection settings
TERMINUSDB_URL = "http://localhost:6363"
TERMINUSDB_USER = "admin"
TERMINUSDB_PASSWORD = "root"


def get_client():
    """Create and return a TerminusDB client"""
    client = Client(TERMINUSDB_URL)
    client.connect(user=TERMINUSDB_USER, key=TERMINUSDB_PASSWORD, team="admin")
    return client


def initialize_database():
    """Initialize the database and schema"""
    print(f"Connecting to TerminusDB at {TERMINUSDB_URL}...")
    client = get_client()
    
    # Check if database exists, delete if it does (for clean setup)
    try:
        if client.get_database(DB_NAME):
            print(f"Database '{DB_NAME}' exists. Deleting for fresh setup...")
            client.delete_database(DB_NAME)
    except Exception as e:
        print(f"Database doesn't exist yet: {e}")
    
    # Create new database
    print(f"Creating database '{DB_NAME}'...")
    client.create_database(DB_NAME, label=DB_LABEL, description=DB_DESCRIPTION)
    
    # Connect to the new database
    print(f"Connecting to database '{DB_NAME}'...")
    client.connect(db=DB_NAME)
    
    print("Database initialized successfully!")
    return client


if __name__ == "__main__":
    try:
        client = initialize_database()
        print(f"\n✓ Database '{DB_NAME}' is ready!")
        print(f"  URL: {TERMINUSDB_URL}")
        print(f"  Name: {DB_NAME}")
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        raise
