"""
Add and Update Examples for the Equipment Database

This script demonstrates how to:
- Add new equipment
- Update existing equipment
- Delete equipment
- Modify equipment properties
"""

from init_db import get_client, DB_NAME
from schema import (
    Manufacturer, Tractor, Combine, ConstructionEquipment,
    EquipmentType, EquipmentCondition
)


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def example_add_manufacturer(client):
    """Example: Add a new manufacturer"""
    print_header("Example 1: Add a New Manufacturer")
    
    new_manufacturer = Manufacturer(
        name="Massey Ferguson",
        country="United States",
        website="https://www.masseyferguson.com"
    )
    
    print(f"Adding manufacturer: {new_manufacturer.name}")
    client.insert_document(new_manufacturer, commit_msg=f"Add manufacturer {new_manufacturer.name}")
    print(f"✓ Successfully added {new_manufacturer.name}\n")


def example_add_tractor(client):
    """Example: Add a new tractor"""
    print_header("Example 2: Add a New Tractor")
    
    new_tractor = Tractor(
        serial_number="MF-7720-2022-005",
        equipment_type=EquipmentType.tractor,
        manufacturer="Manufacturer/Massey Ferguson",
        model="7720",
        year=2022,
        condition=EquipmentCondition.excellent,
        purchase_price=265000.00,
        current_value=255000.00,
        hours_used=320,
        location="South Farm - Barn 3",
        horsepower=235,
        transmission_type="Automatic",
        pto_hp=205,
        lift_capacity=14500,
        four_wheel_drive=True,
        notes="Newly acquired for expansion"
    )
    
    print(f"Adding tractor: {new_tractor.model} ({new_tractor.serial_number})")
    client.insert_document(new_tractor, commit_msg=f"Add tractor {new_tractor.serial_number}")
    print(f"✓ Successfully added {new_tractor.model}\n")
    
    # Verify it was added
    tractors = client.get_all_documents(graph_type="instance", document_template=Tractor)
    matching = [t for t in tractors if t.get('serial_number') == new_tractor.serial_number]
    if matching:
        print(f"Verification: Found tractor in database")
        print(f"  Model: {matching[0].get('model')}")
        print(f"  Year: {matching[0].get('year')}")
        print(f"  Hours: {matching[0].get('hours_used')}")
    print()


def example_add_combine(client):
    """Example: Add a new combine"""
    print_header("Example 3: Add a New Combine")
    
    new_combine = Combine(
        serial_number="CI-8250-2021-003",
        equipment_type=EquipmentType.combine,
        manufacturer="Manufacturer/Case IH",
        model="8250",
        year=2021,
        condition=EquipmentCondition.excellent,
        purchase_price=550000.00,
        current_value=525000.00,
        hours_used=625,
        location="North Farm - Combine Shed",
        header_width=45.0,
        grain_tank_capacity=410,
        horsepower=580,
        separator_type="Rotary",
        notes="Latest model with advanced technology"
    )
    
    print(f"Adding combine: {new_combine.model} ({new_combine.serial_number})")
    client.insert_document(new_combine, commit_msg=f"Add combine {new_combine.serial_number}")
    print(f"✓ Successfully added {new_combine.model}\n")


def example_add_construction_equipment(client):
    """Example: Add new construction equipment"""
    print_header("Example 4: Add New Construction Equipment")
    
    new_equipment = ConstructionEquipment(
        serial_number="CAT-430F-2022-005",
        equipment_type=EquipmentType.backhoe,
        manufacturer="Manufacturer/Caterpillar",
        model="430F Backhoe",
        year=2022,
        condition=EquipmentCondition.excellent,
        purchase_price=115000.00,
        current_value=110000.00,
        hours_used=185,
        location="Construction Yard - Bay 3",
        operating_weight=18000,
        max_digging_depth=16.5,
        max_reach=20.2,
        bucket_capacity=1.1,
        notes="Brand new, minimal usage"
    )
    
    print(f"Adding construction equipment: {new_equipment.model} ({new_equipment.serial_number})")
    client.insert_document(new_equipment, commit_msg=f"Add equipment {new_equipment.serial_number}")
    print(f"✓ Successfully added {new_equipment.model}\n")


def example_update_equipment_hours(client, serial_number, new_hours):
    """Example: Update equipment hours"""
    print_header(f"Example 5: Update Equipment Hours")
    
    print(f"Updating hours for equipment: {serial_number}")
    print(f"New hours: {new_hours}\n")
    
    # Get all equipment and find the one to update
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    equipment = None
    for eq in all_equipment:
        if eq.get('serial_number') == serial_number:
            equipment = eq
            break
    
    if not equipment:
        print(f"✗ Equipment with serial number {serial_number} not found")
        return
    
    print(f"Found: {equipment.get('model')} ({equipment.get('year')})")
    print(f"Current hours: {equipment.get('hours_used', 0)}")
    
    # Update the hours
    equipment['hours_used'] = new_hours
    
    # Replace the document
    client.replace_document(equipment, commit_msg=f"Update hours for {serial_number} to {new_hours}")
    print(f"✓ Successfully updated hours to {new_hours}\n")
    
    # Verify the update
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    for eq in all_equipment:
        if eq.get('serial_number') == serial_number:
            print(f"Verification: Hours now: {eq.get('hours_used')}")
            break
    print()


def example_update_equipment_condition(client, serial_number, new_condition):
    """Example: Update equipment condition"""
    print_header(f"Example 6: Update Equipment Condition")
    
    print(f"Updating condition for equipment: {serial_number}")
    print(f"New condition: {new_condition}\n")
    
    # Get all equipment
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    equipment = None
    for eq in all_equipment:
        if eq.get('serial_number') == serial_number:
            equipment = eq
            break
    
    if not equipment:
        print(f"✗ Equipment with serial number {serial_number} not found")
        return
    
    print(f"Found: {equipment.get('model')} ({equipment.get('year')})")
    print(f"Current condition: {equipment.get('condition')}")
    
    # Update the condition
    equipment['condition'] = new_condition
    
    # Replace the document
    client.replace_document(equipment, commit_msg=f"Update condition for {serial_number} to {new_condition}")
    print(f"✓ Successfully updated condition to {new_condition}\n")


def example_update_equipment_location(client, serial_number, new_location):
    """Example: Update equipment location"""
    print_header(f"Example 7: Update Equipment Location")
    
    print(f"Updating location for equipment: {serial_number}")
    print(f"New location: {new_location}\n")
    
    # Get all equipment
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    equipment = None
    for eq in all_equipment:
        if eq.get('serial_number') == serial_number:
            equipment = eq
            break
    
    if not equipment:
        print(f"✗ Equipment with serial number {serial_number} not found")
        return
    
    print(f"Found: {equipment.get('model')} ({equipment.get('year')})")
    print(f"Current location: {equipment.get('location')}")
    
    # Update the location
    equipment['location'] = new_location
    
    # Replace the document
    client.replace_document(equipment, commit_msg=f"Move {serial_number} to {new_location}")
    print(f"✓ Successfully updated location to {new_location}\n")


def example_update_equipment_value(client, serial_number, new_value):
    """Example: Update equipment current value"""
    print_header(f"Example 8: Update Equipment Value")
    
    print(f"Updating value for equipment: {serial_number}")
    print(f"New value: ${new_value:,.2f}\n")
    
    # Get all equipment
    all_equipment = []
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Tractor))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=Combine))
    all_equipment.extend(client.get_all_documents(graph_type="instance", document_template=ConstructionEquipment))
    
    equipment = None
    for eq in all_equipment:
        if eq.get('serial_number') == serial_number:
            equipment = eq
            break
    
    if not equipment:
        print(f"✗ Equipment with serial number {serial_number} not found")
        return
    
    print(f"Found: {equipment.get('model')} ({equipment.get('year')})")
    print(f"Current value: ${equipment.get('current_value', 0):,.2f}")
    
    # Update the value
    equipment['current_value'] = new_value
    
    # Replace the document
    client.replace_document(equipment, commit_msg=f"Update value for {serial_number} to ${new_value}")
    print(f"✓ Successfully updated value to ${new_value:,.2f}\n")


def example_delete_equipment(client, serial_number):
    """Example: Delete equipment (commented out for safety)"""
    print_header(f"Example 9: Delete Equipment (Demo Only - Not Executed)")
    
    print(f"This example shows how to delete equipment: {serial_number}")
    print("For safety, deletion is not executed in this demo.\n")
    
    print("To delete equipment, use:")
    print("  client.delete_document(document_id)")
    print("\nExample code:")
    print("  # Get the document ID")
    print("  equipment = client.get_document(serial_number)")
    print("  # Delete it")
    print("  client.delete_document(equipment['@id'])")
    print()


def run_all_examples():
    """Run all add/update examples"""
    print("\n" + "=" * 80)
    print("  TERMINUSDB EQUIPMENT DATABASE - ADD/UPDATE EXAMPLES")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Add examples
    example_add_manufacturer(client)
    example_add_tractor(client)
    example_add_combine(client)
    example_add_construction_equipment(client)
    
    # Update examples
    example_update_equipment_hours(client, "JD-8R-370-2020-001", 1350)
    example_update_equipment_condition(client, "CAT-D6T-2017-002", "EquipmentCondition/good")
    example_update_equipment_location(client, "KB-M7-152-2019-002", "North Farm - Barn 2")
    example_update_equipment_value(client, "JD-310-2021-003", 85000.00)
    
    # Delete example (demo only)
    example_delete_equipment(client, "DEMO-SERIAL-001")
    
    print("\n" + "=" * 80)
    print("  All add/update examples completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        run_all_examples()
    except Exception as e:
        print(f"\n✗ Error running add/update examples: {e}")
        raise
