"""
Initialize the TerminusDB Equipment Model Catalog Database

This database focuses on MODEL CONFIGURATIONS rather than individual equipment instances.
It serves as a global reference for all possible equipment models, sub-models, and trims.
"""

from terminusdb_client import Client
from model_catalog_schema import commit_model_catalog_schema


# Database configuration
DB_NAME = "equipment_model_catalog"
DB_LABEL = "Equipment Model Catalog"
DB_DESCRIPTION = "A reference database for equipment model configurations, specifications, and variants"

# TerminusDB connection settings
TERMINUSDB_URL = "http://localhost:6363"
TERMINUSDB_USER = "admin"
TERMINUSDB_PASSWORD = "root"


def get_client():
    """Create and return a TerminusDB client"""
    client = Client(TERMINUSDB_URL)
    client.connect(user=TERMINUSDB_USER, key=TERMINUSDB_PASSWORD, team="admin")
    return client


def initialize_model_catalog():
    """Initialize the model catalog database and schema"""
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
    
    # Commit schema
    print("Creating model catalog schema...")
    commit_model_catalog_schema(client)
    
    print("Model catalog database initialized successfully!")
    return client


if __name__ == "__main__":
    try:
        client = initialize_model_catalog()
        print(f"\n✓ Database '{DB_NAME}' is ready!")
        print(f"  URL: {TERMINUSDB_URL}")
        print(f"  Name: {DB_NAME}")
        print(f"\nThis database is designed for:")
        print("  - Tracking equipment MODEL configurations")
        print("  - Managing model hierarchies (manufacturer → model → trim)")
        print("  - Storing specifications for all available equipment variants")
        print("  - Serving as a global reference for equipment catalogs")
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        raise
