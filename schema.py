"""
TerminusDB Equipment Database Schema

This module defines the schema for an equipment database that includes:
- Tractors
- Combines
- Construction Equipment
- Balers (Small Square, Large Square, and Round)

Using TerminusDB WOQLSchema for proper schema definition
"""

from terminusdb_client import Client
from terminusdb_client.woqlschema import DocumentTemplate, WOQLSchema
from typing import Optional


# Shared schema instance
schema = WOQLSchema()


class Manufacturer(DocumentTemplate):
    """Manufacturer information"""
    _schema = schema
    name: str
    country: str
    website: Optional[str] = None


class Tractor(DocumentTemplate):
    """Tractor equipment"""
    _schema = schema
    serial_number: str
    manufacturer: str
    model: str
    year: int
    condition: str
    horsepower: int
    transmission_type: str
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    hours_used: Optional[int] = 0
    location: Optional[str] = None
    notes: Optional[str] = None
    pto_hp: Optional[int] = None
    lift_capacity: Optional[float] = None
    four_wheel_drive: Optional[bool] = False


class Combine(DocumentTemplate):
    """Combine harvester equipment"""
    _schema = schema
    serial_number: str
    manufacturer: str
    model: str
    year: int
    condition: str
    header_width: float
    grain_tank_capacity: int
    horsepower: int
    separator_type: str
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    hours_used: Optional[int] = 0
    location: Optional[str] = None
    notes: Optional[str] = None


class ConstructionEquipment(DocumentTemplate):
    """Construction equipment"""
    _schema = schema
    serial_number: str
    manufacturer: str
    model: str
    year: int
    condition: str
    equipment_type: str
    operating_weight: float
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    hours_used: Optional[int] = 0
    location: Optional[str] = None
    notes: Optional[str] = None
    max_digging_depth: Optional[float] = None
    max_reach: Optional[float] = None
    bucket_capacity: Optional[float] = None
    max_lift_capacity: Optional[float] = None


class SmallSquareBaler(DocumentTemplate):
    """Small square baler equipment"""
    _schema = schema
    serial_number: str
    manufacturer: str
    model: str
    year: int
    condition: str
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    hours_used: Optional[int] = 0
    location: Optional[str] = None
    notes: Optional[str] = None
    pto_hp_required: Optional[int] = None
    bale_weight_capacity: Optional[float] = None
    bale_width: Optional[float] = None
    bale_height: Optional[float] = None
    bale_length: Optional[float] = None
    bales_per_hour: Optional[int] = None


class LargeSquareBaler(DocumentTemplate):
    """Large square baler equipment"""
    _schema = schema
    serial_number: str
    manufacturer: str
    model: str
    year: int
    condition: str
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    hours_used: Optional[int] = 0
    location: Optional[str] = None
    notes: Optional[str] = None
    pto_hp_required: Optional[int] = None
    bale_weight_capacity: Optional[float] = None
    bale_width: Optional[float] = None
    bale_height: Optional[float] = None
    bale_length: Optional[float] = None
    bales_per_hour: Optional[int] = None
    bale_density: Optional[str] = None


class RoundBaler(DocumentTemplate):
    """Round baler equipment"""
    _schema = schema
    serial_number: str
    manufacturer: str
    model: str
    year: int
    condition: str
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    hours_used: Optional[int] = 0
    location: Optional[str] = None
    notes: Optional[str] = None
    pto_hp_required: Optional[int] = None
    bale_weight_capacity: Optional[float] = None
    bale_diameter: Optional[float] = None
    bale_width: Optional[float] = None
    bales_per_hour: Optional[int] = None
    chamber_type: Optional[str] = None


def commit_schema(client: Client):
    """Commit the schema to the database"""
    schema.commit(client, commit_msg="Create equipment database schema")
    return schema
