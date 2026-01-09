"""
Load sample data into the Equipment Database

This script populates the database with example equipment including:
- Multiple tractors from different manufacturers
- Combine harvesters
- Various construction equipment
"""

from init_db import get_client, DB_NAME
from schema import Manufacturer, Tractor, Combine, ConstructionEquipment


def load_sample_data():
    """Load sample equipment data into the database"""
    print(f"Connecting to database '{DB_NAME}'...")
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Create manufacturers
    print("\nCreating manufacturers...")
    manufacturers = [
        Manufacturer(name="John Deere", country="United States", website="https://www.deere.com"),
        Manufacturer(name="Case IH", country="United States", website="https://www.caseih.com"),
        Manufacturer(name="Caterpillar", country="United States", website="https://www.cat.com"),
        Manufacturer(name="Kubota", country="Japan", website="https://www.kubota.com"),
        Manufacturer(name="New Holland", country="United States", website="https://www.newholland.com"),
    ]
    
    for manufacturer in manufacturers:
        try:
            client.insert_document(manufacturer, commit_msg=f"Add {manufacturer.name}")
            print(f"  ✓ Added {manufacturer.name}")
        except Exception as e:
            print(f"  ! {manufacturer.name} (may already exist): {e}")
    
    # Create tractors
    print("\nCreating tractors...")
    tractors = [
        Tractor(
            serial_number="JD-8R-370-2020-001",
            manufacturer="John Deere",
            model="8R 370",
            year=2020,
            condition="excellent",
            horsepower=370,
            transmission_type="Automatic",
            pto_hp=320,
            lift_capacity=18500.0,
            four_wheel_drive=True,
            purchase_price=385000.00,
            current_value=350000.00,
            hours_used=1250,
            location="North Farm - Barn 1",
            notes="Primary tractor for heavy field work"
        ),
        Tractor(
            serial_number="KB-M7-152-2019-002",
            manufacturer="Kubota",
            model="M7-152",
            year=2019,
            condition="good",
            horsepower=152,
            transmission_type="Hydrostatic",
            pto_hp=130,
            lift_capacity=11000.0,
            four_wheel_drive=True,
            purchase_price=125000.00,
            current_value=105000.00,
            hours_used=2100,
            location="South Farm - Equipment Shed",
            notes="Utility tractor for medium tasks"
        ),
        Tractor(
            serial_number="CI-MAGNUM-340-2021-003",
            manufacturer="Case IH",
            model="Magnum 340",
            year=2021,
            condition="excellent",
            horsepower=340,
            transmission_type="Manual",
            pto_hp=295,
            lift_capacity=17000.0,
            four_wheel_drive=True,
            purchase_price=340000.00,
            current_value=325000.00,
            hours_used=850,
            location="North Farm - Barn 2",
            notes="Recently acquired, low hours"
        ),
    ]
    
    for tractor in tractors:
        try:
            client.insert_document(tractor, commit_msg=f"Add tractor {tractor.serial_number}")
            print(f"  ✓ Added {tractor.model} ({tractor.serial_number})")
        except Exception as e:
            print(f"  ! {tractor.model} (may already exist): {e}")
    
    # Create combines
    print("\nCreating combines...")
    combines = [
        Combine(
            serial_number="JD-S780-2018-001",
            manufacturer="John Deere",
            model="S780",
            year=2018,
            condition="good",
            header_width=40.0,
            grain_tank_capacity=350,
            horsepower=473,
            separator_type="Rotary",
            purchase_price=485000.00,
            current_value=385000.00,
            hours_used=1850,
            location="North Farm - Combine Shed",
            notes="Primary combine for corn and soybeans"
        ),
        Combine(
            serial_number="NH-CR8-90-2020-002",
            manufacturer="New Holland",
            model="CR8.90",
            year=2020,
            condition="excellent",
            header_width=45.0,
            grain_tank_capacity=395,
            horsepower=542,
            separator_type="Hybrid",
            purchase_price=520000.00,
            current_value=475000.00,
            hours_used=950,
            location="South Farm - Equipment Building",
            notes="Backup combine, excellent condition"
        ),
    ]
    
    for combine in combines:
        try:
            client.insert_document(combine, commit_msg=f"Add combine {combine.serial_number}")
            print(f"  ✓ Added {combine.model} ({combine.serial_number})")
        except Exception as e:
            print(f"  ! {combine.model} (may already exist): {e}")
    
    # Create construction equipment
    print("\nCreating construction equipment...")
    construction_equipment = [
        ConstructionEquipment(
            serial_number="CAT-320-2019-001",
            manufacturer="Caterpillar",
            model="320 Excavator",
            year=2019,
            condition="good",
            equipment_type="excavator",
            operating_weight=49800.0,
            max_digging_depth=22.3,
            max_reach=32.5,
            bucket_capacity=1.5,
            purchase_price=185000.00,
            current_value=155000.00,
            hours_used=2750,
            location="Construction Yard - Bay 1",
            notes="Used for drainage and foundation work"
        ),
        ConstructionEquipment(
            serial_number="CAT-D6T-2017-002",
            manufacturer="Caterpillar",
            model="D6T Dozer",
            year=2017,
            condition="fair",
            equipment_type="bulldozer",
            operating_weight=47150.0,
            bucket_capacity=3.5,
            purchase_price=275000.00,
            current_value=195000.00,
            hours_used=4200,
            location="Construction Yard - Bay 2",
            notes="Needs blade replacement soon"
        ),
        ConstructionEquipment(
            serial_number="JD-310-2021-003",
            manufacturer="John Deere",
            model="310L Backhoe",
            year=2021,
            condition="excellent",
            equipment_type="backhoe",
            operating_weight=14500.0,
            max_digging_depth=14.3,
            max_reach=18.1,
            bucket_capacity=0.96,
            purchase_price=95000.00,
            current_value=88000.00,
            hours_used=450,
            location="South Farm - Equipment Shed",
            notes="Multipurpose loader/digger"
        ),
        ConstructionEquipment(
            serial_number="CAT-TL943-2020-004",
            manufacturer="Caterpillar",
            model="TL943 Telehandler",
            year=2020,
            condition="excellent",
            equipment_type="crane",
            operating_weight=24250.0,
            max_reach=43.0,
            max_lift_capacity=9000.0,
            purchase_price=125000.00,
            current_value=115000.00,
            hours_used=780,
            location="North Farm - Barn 1",
            notes="Telescopic handler for barn and construction work"
        ),
    ]
    
    for equipment in construction_equipment:
        try:
            client.insert_document(equipment, commit_msg=f"Add {equipment.equipment_type} {equipment.serial_number}")
            print(f"  ✓ Added {equipment.model} ({equipment.serial_number})")
        except Exception as e:
            print(f"  ! {equipment.model} (may already exist): {e}")
    
    print(f"\n✓ Successfully loaded {len(manufacturers)} manufacturers, {len(tractors)} tractors, "
          f"{len(combines)} combines, and {len(construction_equipment)} construction equipment!")
    
    return client


if __name__ == "__main__":
    try:
        load_sample_data()
        print("\n✓ Sample data loaded successfully!")
    except Exception as e:
        print(f"\n✗ Error loading sample data: {e}")
        import traceback
        traceback.print_exc()
        raise
