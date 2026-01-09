#!/usr/bin/env python3
"""
Main script to run the complete TerminusDB Equipment Database demo

This script:
1. Initializes the database
2. Loads sample data
3. Runs query examples
4. Shows add/update examples
"""

import sys
import time


def print_banner(text):
    """Print a decorative banner"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def check_terminusdb_connection():
    """Check if TerminusDB is running"""
    print("Checking TerminusDB connection...")
    try:
        import requests
        response = requests.get("http://localhost:6363", timeout=5)
        if response.status_code == 200:
            print("✓ TerminusDB is running\n")
            return True
    except Exception as e:
        print(f"✗ Cannot connect to TerminusDB: {e}")
        print("\nPlease start TerminusDB first:")
        print("  docker-compose up -d")
        print("\nThen wait a few seconds and run this script again.\n")
        return False


def run_demo():
    """Run the complete demo"""
    print_banner("TERMINUSDB EQUIPMENT DATABASE - COMPLETE DEMO")
    
    # Check connection
    if not check_terminusdb_connection():
        sys.exit(1)
    
    # Step 1: Initialize database
    print_banner("STEP 1: Initialize Database")
    from init_db import initialize_database
    try:
        initialize_database()
        print("✓ Database initialized successfully!\n")
    except Exception as e:
        print(f"✗ Error initializing database: {e}\n")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 2: Load sample data
    print_banner("STEP 2: Load Sample Data")
    from load_data import load_sample_data
    try:
        load_sample_data()
        print("✓ Sample data loaded successfully!\n")
    except Exception as e:
        print(f"✗ Error loading sample data: {e}\n")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 3: Run queries
    print_banner("STEP 3: Run Query Examples")
    from query_examples import run_all_queries
    try:
        run_all_queries()
        print("✓ Queries completed successfully!\n")
    except Exception as e:
        print(f"✗ Error running queries: {e}\n")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 4: Run add/update examples
    print_banner("STEP 4: Run Add/Update Examples")
    from update_examples import run_all_examples
    try:
        run_all_examples()
        print("✓ Add/Update examples completed successfully!\n")
    except Exception as e:
        print(f"✗ Error running add/update examples: {e}\n")
        sys.exit(1)
    
    # Complete
    print_banner("DEMO COMPLETE!")
    print("The Equipment Database has been successfully set up and demonstrated.")
    print("\nYou can now:")
    print("  - Run individual scripts: init_db.py, load_data.py, query_examples.py, update_examples.py")
    print("  - Access TerminusDB console: http://localhost:6363")
    print("  - Build your own queries and operations using the examples as templates")
    print("\nTo stop TerminusDB:")
    print("  docker compose down")
    print()


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
