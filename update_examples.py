"""
Add and Update Examples for the Equipment Database

This script demonstrates how to:
- Add new equipment
- Update existing equipment  
- Query to verify changes
"""

from init_db import get_client, DB_NAME
from schema import Manufacturer, Tractor, Combine, ConstructionEquipment, SmallSquareBaler, LargeSquareBaler, RoundBaler


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def example_add_tractor(client):
    """Example: Add a new tractor"""
    print_header("Example 1: Add a New Tractor")
    
    new_tractor = Tractor(
        serial_number="KB-M5-111-2023-NEW",
        manufacturer="Kubota",
        model="M5-111",
        year=2023,
        condition="excellent",
        horsepower=111,
        transmission_type="Hydrostatic",
        pto_hp=95,
        lift_capacity=5500.0,
        four_wheel_drive=True,
        purchase_price=85000.00,
        current_value=83000.00,
        hours_used=45,
        location="South Farm - Barn 3",
        notes="Newly acquired compact tractor"
    )
    
    print(f"Adding tractor: {new_tractor.model} ({new_tractor.serial_number})")
    client.insert_document(new_tractor, commit_msg=f"Add tractor {new_tractor.serial_number}")
    print(f"✓ Successfully added {new_tractor.model}\n")


def example_add_combine(client):
    """Example: Add a new combine"""
    print_header("Example 2: Add a New Combine")
    
    new_combine = Combine(
        serial_number="CI-8250-2022-NEW",
        manufacturer="Case IH",
        model="8250 Axial-Flow",
        year=2022,
        condition="excellent",
        header_width=50.0,
        grain_tank_capacity=420,
        horsepower=590,
        separator_type="Rotary",
        purchase_price=565000.00,
        current_value=550000.00,
        hours_used=280,
        location="North Farm - Combine Shed",
        notes="Latest model with precision farming technology"
    )
    
    print(f"Adding combine: {new_combine.model} ({new_combine.serial_number})")
    client.insert_document(new_combine, commit_msg=f"Add combine {new_combine.serial_number}")
    print(f"✓ Successfully added {new_combine.model}\n")


def example_add_round_baler(client):
    """Example: Add a new round baler"""
    print_header("Example 3: Add a New Round Baler")
    
    new_baler = RoundBaler(
        serial_number="CI-RB565-2023-NEW",
        manufacturer="Case IH",
        model="RB565 Premium",
        year=2023,
        condition="excellent",
        pto_hp_required=80,
        bale_weight_capacity=1650.0,
        bale_diameter=62.0,
        bale_width=61.0,
        bales_per_hour=40,
        chamber_type="variable",
        purchase_price=58000.00,
        current_value=57000.00,
        hours_used=75,
        location="North Farm - Barn 3",
        notes="New round baler with CropCutter system"
    )
    
    print(f"Adding round baler: {new_baler.model} ({new_baler.serial_number})")
    client.insert_document(new_baler, commit_msg=f"Add baler {new_baler.serial_number}")
    print(f"✓ Successfully added {new_baler.model}\n")


def example_update_hours(client, serial_number="JD-8R-370-2020-001"):
    """Example: Update equipment hours"""
    print_header(f"Example 4: Update Equipment Hours")
    
    print(f"Finding equipment with serial number: {serial_number}")
    
    # Get all documents and find the one we want
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = None
    for doc in all_docs:
        if doc.get('serial_number') == serial_number:
            equipment = doc
            break
    
    if not equipment:
        print(f"✗ Equipment with serial number {serial_number} not found")
        return
    
    old_hours = equipment.get('hours_used', 0)
    new_hours = old_hours + 100
    
    print(f"Found: {equipment.get('model')} ({equipment.get('year')})")
    print(f"Current hours: {old_hours}")
    print(f"New hours: {new_hours}\n")
    
    # Update the hours
    equipment['hours_used'] = new_hours
    
    # Replace the document
    client.replace_document(equipment, commit_msg=f"Update hours for {serial_number}")
    print(f"✓ Successfully updated hours to {new_hours}\n")


def example_update_location(client, serial_number="CAT-320-2019-001"):
    """Example: Update equipment location"""
    print_header(f"Example 5: Update Equipment Location")
    
    print(f"Finding equipment with serial number: {serial_number}")
    
    # Get all documents and find the one we want
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = None
    for doc in all_docs:
        if doc.get('serial_number') == serial_number:
            equipment = doc
            break
    
    if not equipment:
        print(f"✗ Equipment with serial number {serial_number} not found")
        return
    
    old_location = equipment.get('location', 'Unknown')
    new_location = "Construction Yard - Bay 3 (Maintenance)"
    
    print(f"Found: {equipment.get('model')} ({equipment.get('year')})")
    print(f"Current location: {old_location}")
    print(f"New location: {new_location}\n")
    
    # Update the location
    equipment['location'] = new_location
    equipment['notes'] = equipment.get('notes', '') + " - Moved for scheduled maintenance"
    
    # Replace the document
    client.replace_document(equipment, commit_msg=f"Update location for {serial_number}")
    print(f"✓ Successfully updated location\n")


def example_query_additions(client):
    """Example: Query to see additions"""
    print_header("Example 6: Verify New Additions")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment = [d for d in all_docs if d.get('@type') != 'Manufacturer']
    
    print(f"Total equipment in database: {len(equipment)}\n")
    print("Recently added equipment:")
    
    # Show equipment with less than 500 hours (likely new)
    new_equipment = [e for e in equipment if e.get('hours_used', 0) < 500]
    for e in new_equipment:
        print(f"  - {e.get('model')} ({e.get('year')})")
        print(f"    Hours: {e.get('hours_used', 0)}, Condition: {e.get('condition')}")


def run_all_examples():
    """Run all add/update examples"""
    print("\n" + "=" * 80)
    print("  TERMINUSDB EQUIPMENT DATABASE - ADD/UPDATE EXAMPLES")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Add examples
    example_add_tractor(client)
    example_add_combine(client)
    example_add_round_baler(client)
    
    # Update examples
    example_update_hours(client)
    example_update_location(client)
    
    # Verify
    example_query_additions(client)
    
    print("\n" + "=" * 80)
    print("  All add/update examples completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        run_all_examples()
    except Exception as e:
        print(f"\n✗ Error running add/update examples: {e}")
        import traceback
        traceback.print_exc()
        raise
