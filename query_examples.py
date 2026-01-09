"""
Query Examples for the Equipment Database

This script demonstrates various ways to query the equipment database:
- Get all equipment
- Filter by type
- Query specific information
"""

from init_db import get_client, DB_NAME


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def query_all_equipment(client):
    """Query all equipment in the database"""
    print_header("Query 1: Get All Equipment by Type")
    
    # Query all documents
    all_docs = list(client.get_all_documents(graph_type="instance"))
    
    # Separate by type
    manufacturers = [d for d in all_docs if d.get('@type') == 'Manufacturer']
    tractors = [d for d in all_docs if d.get('@type') == 'Tractor']
    combines = [d for d in all_docs if d.get('@type') == 'Combine']
    construction = [d for d in all_docs if d.get('@type') == 'ConstructionEquipment']
    
    print(f"Manufacturers ({len(manufacturers)}):")
    for m in manufacturers:
        print(f"  - {m.get('name')} ({m.get('country')})")
    
    print(f"\nTractors ({len(tractors)}):")
    for t in tractors:
        print(f"  - {t.get('model')} ({t.get('year')}) - {t.get('hours_used', 0):,} hours")
        print(f"    {t.get('horsepower')} HP, {t.get('transmission_type')}")
    
    print(f"\nCombines ({len(combines)}):")
    for c in combines:
        print(f"  - {c.get('model')} ({c.get('year')}) - {c.get('hours_used', 0):,} hours")
        print(f"    {c.get('header_width')}ft header, {c.get('grain_tank_capacity')} bu capacity")
    
    print(f"\nConstruction Equipment ({len(construction)}):")
    for e in construction:
        print(f"  - {e.get('model')} ({e.get('year')}) - {e.get('equipment_type')}")
        print(f"    {e.get('operating_weight'):,} lbs, {e.get('hours_used', 0):,} hours")


def query_by_condition(client, condition="excellent"):
    """Query equipment by condition"""
    print_header(f"Query 2: Equipment in '{condition}' Condition")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = [d for d in all_docs if d.get('condition') == condition and d.get('@type') != 'Manufacturer']
    
    print(f"Found {len(equipment)} items in {condition} condition:\n")
    for e in equipment:
        value = e.get('current_value')
        value_str = f"${value:,.2f}" if value else "N/A"
        print(f"  - {e.get('model')} ({e.get('year')})")
        print(f"    Type: {e.get('@type')}, Value: {value_str}")
        print(f"    Location: {e.get('location', 'Not specified')}")


def query_high_value(client, min_value=200000):
    """Query high-value equipment"""
    print_header(f"Query 3: Equipment Valued Over ${min_value:,}")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = [d for d in all_docs 
                if d.get('current_value') and d.get('current_value') >= min_value]
    
    # Sort by value
    equipment.sort(key=lambda x: x.get('current_value', 0), reverse=True)
    
    total_value = sum(e.get('current_value', 0) for e in equipment)
    
    print(f"Found {len(equipment)} items:\n")
    for e in equipment:
        print(f"  - {e.get('model')} ({e.get('year')}): ${e.get('current_value'):,.2f}")
        print(f"    Type: {e.get('@type')}, Location: {e.get('location', 'N/A')}")
    
    print(f"\nTotal Value: ${total_value:,.2f}")


def query_by_manufacturer(client, manufacturer="John Deere"):
    """Query equipment by manufacturer"""
    print_header(f"Query 4: {manufacturer} Equipment")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = [d for d in all_docs 
                if d.get('manufacturer') == manufacturer and d.get('@type') != 'Manufacturer']
    
    print(f"Found {len(equipment)} {manufacturer} items:\n")
    for e in equipment:
        print(f"  - {e.get('model')} ({e.get('year')})")
        print(f"    Type: {e.get('@type')}, Serial: {e.get('serial_number')}")
        print(f"    Hours: {e.get('hours_used', 0):,}, Condition: {e.get('condition')}")


def query_summary(client):
    """Get equipment summary statistics"""
    print_header("Query 5: Equipment Fleet Summary")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = [d for d in all_docs if d.get('@type') != 'Manufacturer']
    
    # Count by type
    type_counts = {}
    for e in equipment:
        t = e.get('@type')
        type_counts[t] = type_counts.get(t, 0) + 1
    
    # Financial summary
    total_purchase = sum(e.get('purchase_price', 0) for e in equipment)
    total_current = sum(e.get('current_value', 0) for e in equipment)
    total_hours = sum(e.get('hours_used', 0) for e in equipment)
    
    print(f"Total Equipment: {len(equipment)} items\n")
    print("By Type:")
    for t, count in type_counts.items():
        print(f"  - {t}: {count}")
    
    print(f"\nFinancial Summary:")
    print(f"  - Total Purchase Price: ${total_purchase:,.2f}")
    print(f"  - Total Current Value: ${total_current:,.2f}")
    print(f"  - Total Depreciation: ${total_purchase - total_current:,.2f}")
    
    print(f"\nUsage Summary:")
    print(f"  - Total Hours: {total_hours:,}")
    print(f"  - Average Hours per Item: {total_hours / len(equipment) if equipment else 0:.0f}")


def run_all_queries():
    """Run all example queries"""
    print("\n" + "=" * 80)
    print("  TERMINUSDB EQUIPMENT DATABASE - QUERY EXAMPLES")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Run example queries
    query_all_equipment(client)
    query_by_condition(client, "excellent")
    query_high_value(client, 200000)
    query_by_manufacturer(client, "John Deere")
    query_summary(client)
    
    print("\n" + "=" * 80)
    print("  All queries completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        run_all_queries()
    except Exception as e:
        print(f"\n✗ Error running queries: {e}")
        import traceback
        traceback.print_exc()
        raise
