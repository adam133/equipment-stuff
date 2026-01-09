"""
TerminusDB Equipment Database Schema

This module defines the schema for an equipment database that includes:
- Tractors
- Combines
- Construction Equipment
"""

from terminusdb_client import Client
from terminusdb_client.woqlschema import DocumentTemplate, EnumTemplate, LexicalKey


class EquipmentType(EnumTemplate):
    """Types of equipment in the database"""
    tractor = ()
    combine = ()
    excavator = ()
    bulldozer = ()
    backhoe = ()
    crane = ()


class EquipmentCondition(EnumTemplate):
    """Condition status of equipment"""
    excellent = ()
    good = ()
    fair = ()
    poor = ()
    needs_repair = ()


class Manufacturer(DocumentTemplate):
    """Manufacturer information"""
    _key = LexicalKey(['name'])
    name: str
    country: str
    website: str = None


class Equipment(DocumentTemplate):
    """Base equipment class"""
    _key = LexicalKey(['serial_number'])
    serial_number: str
    equipment_type: EquipmentType
    manufacturer: Manufacturer
    model: str
    year: int
    condition: EquipmentCondition
    purchase_price: float = None
    current_value: float = None
    hours_used: int = 0
    location: str = None
    notes: str = None


class Tractor(Equipment):
    """Tractor-specific attributes"""
    horsepower: int
    transmission_type: str  # Manual, Automatic, Hydrostatic
    pto_hp: int = None  # Power Take-Off horsepower
    lift_capacity: float = None  # in lbs
    four_wheel_drive: bool = False


class Combine(Equipment):
    """Combine harvester-specific attributes"""
    header_width: float  # in feet
    grain_tank_capacity: int  # in bushels
    horsepower: int
    separator_type: str  # Conventional, Rotary, Hybrid


class ConstructionEquipment(Equipment):
    """Construction equipment-specific attributes"""
    operating_weight: float  # in lbs
    max_digging_depth: float = None  # in feet
    max_reach: float = None  # in feet
    bucket_capacity: float = None  # in cubic yards
    max_lift_capacity: float = None  # in lbs for cranes


def create_schema(client: Client):
    """Create the database schema"""
    # The schema is automatically created when classes are defined
    # This function exists to organize schema creation
    schema_classes = [
        EquipmentType,
        EquipmentCondition,
        Manufacturer,
        Equipment,
        Tractor,
        Combine,
        ConstructionEquipment
    ]
    
    # Insert schema objects into the database
    for schema_class in schema_classes:
        client.insert_document(schema_class(), graph_type="schema")
    
    return schema_classes
