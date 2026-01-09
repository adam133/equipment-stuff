"""
TerminusDB Equipment Model Catalog Schema

This module defines a schema focused on equipment MODEL CONFIGURATIONS
rather than individual equipment instances. This is designed as a 
global reference for all possible equipment models, sub-models, and trims.

Key differences from instance tracking:
- Focus on MODEL specifications and configurations
- Track all available variants and options
- No individual serial numbers or usage tracking
- Designed for reference data, not operational data
"""

from terminusdb_client import Client
from terminusdb_client.woqlschema import DocumentTemplate, WOQLSchema, TaggedUnion
from typing import Optional, List
from enum import Enum


# Shared schema instance for model catalog
model_schema = WOQLSchema()


class PowertrainType(Enum):
    """Types of powertrains available"""
    diesel = "diesel"
    gasoline = "gasoline"
    hybrid_diesel_electric = "hybrid_diesel_electric"
    electric = "electric"
    lpg = "lpg"
    dual_fuel = "dual_fuel"


class TransmissionType(Enum):
    """Types of transmissions"""
    manual = "manual"
    automatic = "automatic"
    hydrostatic = "hydrostatic"
    cvt = "cvt"  # Continuously Variable Transmission
    powershift = "powershift"


class ManufacturerCatalog(DocumentTemplate):
    """Manufacturer information for model catalog"""
    _schema = model_schema
    name: str
    country: str
    founded_year: Optional[int] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    product_categories: Optional[List[str]] = None


class EngineSpecification(DocumentTemplate):
    """Engine specifications for a model"""
    _schema = model_schema
    displacement_liters: float
    cylinders: int
    configuration: str  # e.g., "Inline-4", "V6", "Inline-6"
    aspiration: str  # "Naturally Aspirated", "Turbocharged", "Twin-Turbo"
    fuel_type: str
    max_power_hp: int
    max_power_rpm: int
    max_torque_nm: int
    max_torque_rpm: int
    emissions_tier: Optional[str] = None  # e.g., "Tier 4 Final", "Stage V"


class HydraulicSpecification(DocumentTemplate):
    """Hydraulic system specifications"""
    _schema = model_schema
    pump_flow_rate_lpm: float  # Liters per minute
    system_pressure_bar: int
    remote_valve_count: int
    lift_capacity_rear_kg: Optional[float] = None
    lift_capacity_front_kg: Optional[float] = None


class DimensionSpecification(DocumentTemplate):
    """Physical dimensions of equipment"""
    _schema = model_schema
    length_mm: int
    width_mm: int
    height_mm: int
    wheelbase_mm: int
    ground_clearance_mm: int
    turning_radius_m: float
    operating_weight_kg: int
    shipping_weight_kg: Optional[int] = None


class TractorModel(DocumentTemplate):
    """
    Tractor model configuration (not an instance).
    Represents a specific model that can have multiple trims/variants.
    """
    _schema = model_schema
    manufacturer: str  # Reference to ManufacturerCatalog
    model_name: str
    model_year: int
    series: Optional[str] = None  # e.g., "8R Series", "M7 Series"
    
    # Core specifications
    engine: str  # Reference to EngineSpecification
    rated_power_hp: int
    pto_power_hp: Optional[int] = None
    transmission_type: str
    transmission_speeds: Optional[str] = None  # e.g., "16F/16R", "Infinitely Variable"
    four_wheel_drive: bool
    
    # Hydraulics
    hydraulics: Optional[str] = None  # Reference to HydraulicSpecification
    
    # Dimensions
    dimensions: Optional[str] = None  # Reference to DimensionSpecification
    
    # Capacities
    fuel_capacity_liters: Optional[int] = None
    def_capacity_liters: Optional[int] = None  # Diesel Exhaust Fluid
    
    # Features and options
    standard_features: Optional[List[str]] = None
    optional_features: Optional[List[str]] = None
    available_tire_sizes: Optional[List[str]] = None
    
    # Production info
    production_start_date: Optional[str] = None
    production_end_date: Optional[str] = None
    replaced_by_model: Optional[str] = None
    replaces_model: Optional[str] = None
    
    # Metadata
    msrp_base_usd: Optional[float] = None
    category: Optional[str] = None  # e.g., "Compact Utility", "Row Crop", "High Horsepower"


class TractorTrim(DocumentTemplate):
    """
    Specific trim/variant of a tractor model.
    Represents different configurations of the same base model.
    """
    _schema = model_schema
    base_model: str  # Reference to TractorModel
    trim_name: str  # e.g., "Premium", "Deluxe", "Base"
    trim_code: Optional[str] = None  # Manufacturer's trim code
    
    # Trim-specific specifications
    horsepower_variant: Optional[int] = None  # If different from base
    transmission_variant: Optional[str] = None
    hydraulic_variant: Optional[str] = None
    
    # Included features for this trim
    included_features: Optional[List[str]] = None
    excluded_features: Optional[List[str]] = None
    
    # Pricing
    msrp_usd: Optional[float] = None
    trim_premium_usd: Optional[float] = None  # Price difference from base


class CombineModel(DocumentTemplate):
    """Combine harvester model configuration"""
    _schema = model_schema
    manufacturer: str
    model_name: str
    model_year: int
    series: Optional[str] = None
    
    # Engine
    engine: str
    rated_power_hp: int
    
    # Harvesting specifications
    separator_type: str  # "Conventional", "Rotary", "Hybrid"
    separator_width_mm: Optional[int] = None
    grain_tank_capacity_liters: int
    unloading_rate_liters_per_sec: Optional[float] = None
    
    # Compatible headers
    compatible_header_types: Optional[List[str]] = None
    compatible_header_widths_m: Optional[List[float]] = None
    
    # Dimensions
    dimensions: Optional[str] = None
    
    # Features
    standard_features: Optional[List[str]] = None
    optional_features: Optional[List[str]] = None
    
    # Production
    production_start_date: Optional[str] = None
    production_end_date: Optional[str] = None
    msrp_base_usd: Optional[float] = None


class BalerModel(DocumentTemplate):
    """Base baler model configuration"""
    _schema = model_schema
    manufacturer: str
    model_name: str
    model_year: int
    baler_type: str  # "Small Square", "Large Square", "Round"
    
    # Power requirements
    pto_hp_required_min: int
    pto_hp_required_recommended: int
    pto_speed_rpm: int
    
    # Bale specifications
    bale_weight_capacity_kg: float
    bales_per_hour_typical: int
    bales_per_hour_max: Optional[int] = None
    
    # Dimensions
    dimensions: Optional[str] = None
    transport_width_mm: Optional[int] = None
    transport_height_mm: Optional[int] = None
    
    # Features
    twine_systems: Optional[List[str]] = None
    wrap_systems: Optional[List[str]] = None
    standard_features: Optional[List[str]] = None
    optional_features: Optional[List[str]] = None
    
    # Production
    production_start_date: Optional[str] = None
    production_end_date: Optional[str] = None
    msrp_base_usd: Optional[float] = None


class RoundBalerModel(BalerModel):
    """Round baler specific model configuration"""
    _schema = model_schema
    chamber_type: str  # "Fixed", "Variable"
    bale_diameter_min_cm: int
    bale_diameter_max_cm: int
    bale_width_cm: int


class SquareBalerModel(BalerModel):
    """Square baler specific model configuration"""
    _schema = model_schema
    bale_width_cm: int
    bale_height_cm: int
    bale_length_cm: int
    bale_density_kg_per_m3: Optional[int] = None
    compression_type: Optional[str] = None


class ConstructionEquipmentModel(DocumentTemplate):
    """Construction equipment model configuration"""
    _schema = model_schema
    manufacturer: str
    model_name: str
    model_year: int
    equipment_category: str  # "Excavator", "Dozer", "Wheel Loader", etc.
    size_class: Optional[str] = None  # "Compact", "Mid-Size", "Large"
    
    # Engine
    engine: str
    rated_power_hp: int
    
    # Performance specs
    operating_weight_kg: int
    bucket_capacity_m3: Optional[float] = None
    max_dig_depth_m: Optional[float] = None
    max_reach_m: Optional[float] = None
    max_lift_capacity_kg: Optional[float] = None
    blade_capacity_m3: Optional[float] = None
    
    # Dimensions
    dimensions: Optional[str] = None
    
    # Features
    standard_features: Optional[List[str]] = None
    optional_features: Optional[List[str]] = None
    available_attachments: Optional[List[str]] = None
    
    # Production
    production_start_date: Optional[str] = None
    production_end_date: Optional[str] = None
    msrp_base_usd: Optional[float] = None


def commit_model_catalog_schema(client: Client):
    """Commit the model catalog schema to the database"""
    model_schema.commit(client, commit_msg="Create equipment model catalog schema")
    return model_schema
