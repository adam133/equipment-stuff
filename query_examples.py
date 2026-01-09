"""
Query Examples for the Equipment Database

This script demonstrates various ways to query the equipment database:
- Get all equipment
- Filter by type
- Filter by manufacturer
- Filter by condition
- Get equipment by price range
- Get equipment by hours used
- Complex queries combining multiple criteria
"""

from init_db import get_client, DB_NAME
from schema import Tractor, Combine, ConstructionEquipment, Manufacturer
import json


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def print_equipment(equipment_list, label="Equipment"):
    """Pretty print equipment details"""
    if not equipment_list:
        print(f"  No {label} found.")
        return
    
    print(f"Found {len(equipment_list)} {label}:\n")
    for i, equipment in enumerate(equipment_list, 1):
        print(f"{i}. {equipment.get('model', 'Unknown')} ({equipment.get('year', 'N/A')})")
        print(f"   Serial: {equipment.get('serial_number', 'N/A')}")
        print(f"   Type: {equipment.get('equipment_type', 'N/A')}")
        print(f"   Condition: {equipment.get('condition', 'N/A')}")
        print(f"   Hours: {equipment.get('hours_used', 0):,}")
        print(f"   Location: {equipment.get('location', 'N/A')}")
        if equipment.get('current_value'):
            print(f"   Value: ${equipment.get('current_value', 0):,.2f}")
        print()


def query_all_equipment(client):
    """Query all equipment in the database"""
    print_header("Query 1: Get All Equipment")
    
    # Query tractors
    tractors = client.get_all_documents(graph_type="instance", document_template=Tractor)
    print_equipment(tractors, "Tractors")
    
    # Query combines
    combines = client.get_all_documents(graph_type="instance", document_template=Combine)
    print_equipment(combines, "Combines")
    
    # Query construction equipment
    construction = client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment)
    print_equipment(construction, "Construction Equipment")


def query_by_manufacturer(client, manufacturer_name):
    """Query equipment by manufacturer"""
    print_header(f"Query 2: Get Equipment by Manufacturer ({manufacturer_name})")
    
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    # Filter by manufacturer
    filtered = [eq for eq in all_equipment 
                if manufacturer_name.lower() in str(eq.get('manufacturer', '')).lower()]
    
    print_equipment(filtered, f"{manufacturer_name} Equipment")


def query_by_condition(client, condition):
    """Query equipment by condition"""
    print_header(f"Query 3: Get Equipment by Condition ({condition})")
    
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    # Filter by condition
    filtered = [eq for eq in all_equipment 
                if condition.lower() in str(eq.get('condition', '')).lower()]
    
    print_equipment(filtered, f"{condition.title()} Condition Equipment")


def query_high_value_equipment(client, min_value=200000):
    """Query equipment above a certain value"""
    print_header(f"Query 4: Get High-Value Equipment (>${min_value:,})")
    
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    # Filter by current value
    filtered = [eq for eq in all_equipment 
                if eq.get('current_value', 0) >= min_value]
    
    # Sort by value (descending)
    filtered.sort(key=lambda x: x.get('current_value', 0), reverse=True)
    
    print_equipment(filtered, f"High-Value Equipment")
    
    if filtered:
        total_value = sum(eq.get('current_value', 0) for eq in filtered)
        print(f"Total Value: ${total_value:,.2f}\n")


def query_low_hours_equipment(client, max_hours=1500):
    """Query equipment with low hours"""
    print_header(f"Query 5: Get Low-Hours Equipment (<{max_hours:,} hours)")
    
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    # Filter by hours
    filtered = [eq for eq in all_equipment 
                if eq.get('hours_used', 0) < max_hours]
    
    # Sort by hours (ascending)
    filtered.sort(key=lambda x: x.get('hours_used', 0))
    
    print_equipment(filtered, f"Low-Hours Equipment")


def query_by_location(client, location_keyword):
    """Query equipment by location"""
    print_header(f"Query 6: Get Equipment by Location (containing '{location_keyword}')")
    
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    # Filter by location
    filtered = [eq for eq in all_equipment 
                if location_keyword.lower() in str(eq.get('location', '')).lower()]
    
    print_equipment(filtered, f"Equipment at '{location_keyword}'")


def query_recent_equipment(client, min_year=2020):
    """Query recently purchased equipment"""
    print_header(f"Query 7: Get Recent Equipment (Year >= {min_year})")
    
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    # Filter by year
    filtered = [eq for eq in all_equipment 
                if eq.get('year', 0) >= min_year]
    
    # Sort by year (descending)
    filtered.sort(key=lambda x: x.get('year', 0), reverse=True)
    
    print_equipment(filtered, f"Recent Equipment")


def query_manufacturers(client):
    """Query all manufacturers"""
    print_header("Query 8: Get All Manufacturers")
    
    manufacturers = client.get_all_documents(graph_type="instance", document_template=Manufacturer)
    
    if not manufacturers:
        print("  No manufacturers found.")
        return
    
    print(f"Found {len(manufacturers)} manufacturers:\n")
    for i, mfr in enumerate(manufacturers, 1):
        print(f"{i}. {mfr.get('name', 'Unknown')}")
        print(f"   Country: {mfr.get('country', 'N/A')}")
        print(f"   Website: {mfr.get('website', 'N/A')}")
        print()


def query_equipment_summary(client):
    """Get a summary of all equipment"""
    print_header("Query 9: Equipment Summary Statistics")
    
    tractors = client.get_all_documents(graph_type="instance", document_template=Tractor)
    combines = client.get_all_documents(graph_type="instance", document_template=Combine)
    construction = client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment)
    
    all_equipment = tractors + combines + construction
    
    print(f"Total Equipment Count: {len(all_equipment)}")
    print(f"  - Tractors: {len(tractors)}")
    print(f"  - Combines: {len(combines)}")
    print(f"  - Construction Equipment: {len(construction)}")
    print()
    
    # Calculate total values
    total_purchase = sum(eq.get('purchase_price', 0) for eq in all_equipment if eq.get('purchase_price'))
    total_current = sum(eq.get('current_value', 0) for eq in all_equipment if eq.get('current_value'))
    total_hours = sum(eq.get('hours_used', 0) for eq in all_equipment)
    
    print(f"Financial Summary:")
    print(f"  - Total Purchase Price: ${total_purchase:,.2f}")
    print(f"  - Total Current Value: ${total_current:,.2f}")
    print(f"  - Total Depreciation: ${total_purchase - total_current:,.2f}")
    print()
    
    print(f"Usage Summary:")
    print(f"  - Total Hours Used: {total_hours:,}")
    print(f"  - Average Hours per Equipment: {total_hours / len(all_equipment) if all_equipment else 0:,.0f}")
    print()


def run_all_queries():
    """Run all example queries"""
    print("\n" + "=" * 80)
    print("  TERMINUSDB EQUIPMENT DATABASE - QUERY EXAMPLES")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Run all example queries
    query_all_equipment(client)
    query_by_manufacturer(client, "John Deere")
    query_by_condition(client, "excellent")
    query_high_value_equipment(client, 200000)
    query_low_hours_equipment(client, 1500)
    query_by_location(client, "North Farm")
    query_recent_equipment(client, 2020)
    query_manufacturers(client)
    query_equipment_summary(client)
    
    print("\n" + "=" * 80)
    print("  All queries completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        run_all_queries()
    except Exception as e:
        print(f"\n✗ Error running queries: {e}")
        raise
