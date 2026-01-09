"""
Load Equipment Model Catalog Data

This script populates the model catalog with comprehensive equipment model data,
including manufacturers, models, trims, and detailed specifications.

Focus is on MODEL CONFIGURATIONS, not individual equipment instances.
"""

from init_model_catalog import get_client, DB_NAME
from model_catalog_schema import (
    ManufacturerCatalog, TractorModel, TractorTrim, CombineModel,
    RoundBalerModel, SquareBalerModel, ConstructionEquipmentModel,
    EngineSpecification, HydraulicSpecification, DimensionSpecification
)


def load_manufacturers(client):
    """Load manufacturer catalog data"""
    print("\nLoading manufacturers...")
    manufacturers = [
        ManufacturerCatalog(
            name="John Deere",
            country="United States",
            founded_year=1837,
            headquarters="Moline, Illinois",
            website="https://www.deere.com",
            product_categories="Tractors, Combines, Construction Equipment, Hay Equipment"
        ),
        ManufacturerCatalog(
            name="Case IH",
            country="United States",
            founded_year=1842,
            headquarters="Racine, Wisconsin",
            website="https://www.caseih.com",
            product_categories="Tractors, Combines, Hay Equipment"
        ),
        ManufacturerCatalog(
            name="New Holland",
            country="United States",
            founded_year=1895,
            headquarters="New Holland, Pennsylvania",
            website="https://www.newholland.com",
            product_categories="Tractors, Combines, Hay Equipment, Construction Equipment"
        ),
        ManufacturerCatalog(
            name="Kubota",
            country="Japan",
            founded_year=1890,
            headquarters="Osaka, Japan",
            website="https://www.kubota.com",
            product_categories="Tractors, Construction Equipment, Utility Vehicles"
        ),
        ManufacturerCatalog(
            name="Caterpillar",
            country="United States",
            founded_year=1925,
            headquarters="Peoria, Illinois",
            website="https://www.cat.com",
            product_categories="Construction Equipment, Mining Equipment, Engines"
        ),
    ]
    
    for mfr in manufacturers:
        try:
            client.insert_document(mfr, commit_msg=f"Add manufacturer {mfr.name}")
            print(f"  ✓ Added {mfr.name}")
        except Exception as e:
            print(f"  ! {mfr.name}: {e}")


def load_engine_specs(client):
    """Load engine specifications"""
    print("\nLoading engine specifications...")
    engines = [
        EngineSpecification(
            displacement_liters=9.0,
            cylinders=6,
            configuration="Inline-6",
            aspiration="Turbocharged with Intercooler",
            fuel_type="Diesel",
            max_power_hp=370,
            max_power_rpm=2100,
            max_torque_nm=1896,
            max_torque_rpm=1400,
            emissions_tier="Tier 4 Final"
        ),
        EngineSpecification(
            displacement_liters=6.8,
            cylinders=6,
            configuration="Inline-6",
            aspiration="Turbocharged",
            fuel_type="Diesel",
            max_power_hp=340,
            max_power_rpm=2200,
            max_torque_nm=1695,
            max_torque_rpm=1500,
            emissions_tier="Tier 4 Final"
        ),
        EngineSpecification(
            displacement_liters=4.5,
            cylinders=4,
            configuration="Inline-4",
            aspiration="Turbocharged",
            fuel_type="Diesel",
            max_power_hp=152,
            max_power_rpm=2300,
            max_torque_nm=690,
            max_torque_rpm=1600,
            emissions_tier="Tier 4 Final"
        ),
        EngineSpecification(
            displacement_liters=13.6,
            cylinders=6,
            configuration="Inline-6",
            aspiration="Turbocharged with Intercooler",
            fuel_type="Diesel",
            max_power_hp=473,
            max_power_rpm=2100,
            max_torque_nm=2380,
            max_torque_rpm=1400,
            emissions_tier="Tier 4 Final"
        ),
    ]
    
    for i, engine in enumerate(engines):
        try:
            client.insert_document(engine, commit_msg=f"Add engine specification {i+1}")
            print(f"  ✓ Added {engine.max_power_hp}HP engine")
        except Exception as e:
            print(f"  ! Engine {i+1}: {e}")


def load_hydraulic_specs(client):
    """Load hydraulic specifications"""
    print("\nLoading hydraulic specifications...")
    hydraulics = [
        HydraulicSpecification(
            pump_flow_rate_lpm=227,
            system_pressure_bar=241,
            remote_valve_count=5,
            lift_capacity_rear_kg=8391,
            lift_capacity_front_kg=4536
        ),
        HydraulicSpecification(
            pump_flow_rate_lpm=159,
            system_pressure_bar=207,
            remote_valve_count=4,
            lift_capacity_rear_kg=4990,
            lift_capacity_front_kg=2722
        ),
    ]
    
    for i, hyd in enumerate(hydraulics):
        try:
            client.insert_document(hyd, commit_msg=f"Add hydraulic specification {i+1}")
            print(f"  ✓ Added hydraulic spec {i+1}")
        except Exception as e:
            print(f"  ! Hydraulic {i+1}: {e}")


def load_dimension_specs(client):
    """Load dimension specifications"""
    print("\nLoading dimension specifications...")
    dimensions = [
        DimensionSpecification(
            length_mm=6045,
            width_mm=2692,
            height_mm=3480,
            wheelbase_mm=3225,
            ground_clearance_mm=575,
            turning_radius_m=5.18,
            operating_weight_kg=12700,
            shipping_weight_kg=11340
        ),
        DimensionSpecification(
            length_mm=4750,
            width_mm=2350,
            height_mm=2950,
            wheelbase_mm=2640,
            ground_clearance_mm=450,
            turning_radius_m=4.20,
            operating_weight_kg=5800,
            shipping_weight_kg=5200
        ),
    ]
    
    for i, dim in enumerate(dimensions):
        try:
            client.insert_document(dim, commit_msg=f"Add dimension specification {i+1}")
            print(f"  ✓ Added dimension spec {i+1}")
        except Exception as e:
            print(f"  ! Dimension {i+1}: {e}")


def load_tractor_models(client):
    """Load tractor model configurations"""
    print("\nLoading tractor models...")
    
    # Get references to manufacturers (in a real system, you'd query these)
    john_deere = "John Deere"
    case_ih = "Case IH"
    kubota = "Kubota"
    
    models = [
        TractorModel(
            manufacturer=john_deere,
            model_name="8R 370",
            model_year=2024,
            series="8R Series",
            engine="EngineSpecification/1",
            rated_power_hp=370,
            pto_power_hp=320,
            transmission_type="Infinitely Variable",
            transmission_speeds="Infinitely Variable (IVT)",
            four_wheel_drive=True,
            hydraulics="HydraulicSpecification/1",
            dimensions="DimensionSpecification/1",
            fuel_capacity_liters=1135,
            def_capacity_liters=76,
            standard_features="CommandCenter 4 Display, AutoTrac Ready, Premium LED Lighting, Air Suspension Seat, Hydraulic Trailer Brakes",
            optional_features="AutoTrac Activation, JDLink Telematics, Premium Cab Soundproofing, Twin Wheel Configuration, Front 3-Point Hitch",
            available_tire_sizes="480/80R50, 520/85R46, 480/80R46",
            production_start_date="2023-08-01",
            msrp_base_usd=385000.00,
            category="Row Crop"
        ),
        TractorModel(
            manufacturer=case_ih,
            model_name="Magnum 340",
            model_year=2024,
            series="Magnum Series",
            engine="EngineSpecification/2",
            rated_power_hp=340,
            pto_power_hp=295,
            transmission_type="Continuously Variable",
            transmission_speeds="CVXDrive (Continuously Variable)",
            four_wheel_drive=True,
            fuel_capacity_liters=1173,
            def_capacity_liters=83,
            standard_features="AFS Pro 1200 Display, Deluxe Cab with Air Suspension, LED Work Lights, AccuGuide Ready",
            optional_features="AccuGuide Activation, Advanced Farming Systems (AFS), Front Linkage and PTO, Rear Wheel Weights",
            production_start_date="2023-06-01",
            msrp_base_usd=340000.00,
            category="Row Crop"
        ),
        TractorModel(
            manufacturer=kubota,
            model_name="M7-152",
            model_year=2024,
            series="M7 Series",
            engine="EngineSpecification/3",
            rated_power_hp=152,
            pto_power_hp=130,
            transmission_type="Hydrostatic",
            transmission_speeds="Infinitely Variable (HMT)",
            four_wheel_drive=True,
            fuel_capacity_liters=270,
            def_capacity_liters=30,
            standard_features="Kubota Multi-Info Display, Bi-Speed Turn, Auto PTO, Cruise Control",
            optional_features="Kubota Farm Solutions (KFS), Front Loader Ready Package, LED Work Light Package, Air Suspension Seat",
            production_start_date="2023-01-01",
            msrp_base_usd=125000.00,
            category="Utility"
        ),
    ]
    
    for model in models:
        try:
            client.insert_document(model, commit_msg=f"Add tractor model {model.model_name}")
            print(f"  ✓ Added {model.manufacturer} {model.model_name}")
        except Exception as e:
            print(f"  ! {model.model_name}: {e}")


def load_tractor_trims(client):
    """Load tractor trim/variant configurations"""
    print("\nLoading tractor trims...")
    
    trims = [
        TractorTrim(
            base_model="TractorModel/1",  # 8R 370
            trim_name="Base",
            trim_code="8R370-BASE",
            included_features="CommandCenter 4 Display, AutoTrac Ready, Premium LED Lighting",
            msrp_usd=385000.00,
            trim_premium_usd=0.00
        ),
        TractorTrim(
            base_model="TractorModel/1",  # 8R 370
            trim_name="Premium",
            trim_code="8R370-PREM",
            included_features="CommandCenter 4 Display with Premium Features, AutoTrac Activated, Premium LED Lighting Package, JDLink Telematics - 3 Years, Premium Cab Soundproofing, Leather Seat",
            msrp_usd=425000.00,
            trim_premium_usd=40000.00
        ),
        TractorTrim(
            base_model="TractorModel/2",  # Magnum 340
            trim_name="Base",
            trim_code="MAG340-BASE",
            included_features="AFS Pro 1200 Display, Deluxe Cab, LED Work Lights",
            msrp_usd=340000.00,
            trim_premium_usd=0.00
        ),
        TractorTrim(
            base_model="TractorModel/2",  # Magnum 340
            trim_name="Rowtrac",
            trim_code="MAG340-ROWTRAC",
            hydraulic_variant="Enhanced Hydraulic System - 295 LPM",
            included_features="AFS Pro 1200 Display, Rowtrac Rubber Track System, Premium Cab Package, AccuGuide Ready",
            msrp_usd=395000.00,
            trim_premium_usd=55000.00
        ),
    ]
    
    for trim in trims:
        try:
            client.insert_document(trim, commit_msg=f"Add tractor trim {trim.trim_name}")
            print(f"  ✓ Added trim: {trim.trim_name} ({trim.trim_code})")
        except Exception as e:
            print(f"  ! Trim {trim.trim_name}: {e}")


def load_combine_models(client):
    """Load combine model configurations"""
    print("\nLoading combine models...")
    
    models = [
        CombineModel(
            manufacturer="John Deere",
            model_name="S780",
            model_year=2024,
            series="S-Series",
            engine="EngineSpecification/4",
            rated_power_hp=473,
            separator_type="Rotary",
            separator_width_mm=1600,
            grain_tank_capacity_liters=14100,
            unloading_rate_liters_per_sec=159,
            compatible_header_types="Grain Platform, Corn Head, Draper Platform, Flex Draper, Contour Master",
            compatible_header_widths_m="9.1, 10.7, 12.2, 13.7",
            standard_features="Generation 4 CommandCenter Display, ProDrive Transmission, Active Terrain Adjustment, Dyna-Flo Plus Cleaning System",
            optional_features="HarvestLab 3000 Grain Sensing, Active Yield and Moisture Calibration, Machine Sync, Combine Advisor Package",
            production_start_date="2023-07-01",
            msrp_base_usd=485000.00
        ),
        CombineModel(
            manufacturer="Case IH",
            model_name="8250 Axial-Flow",
            model_year=2024,
            series="Axial-Flow 250 Series",
            engine="EngineSpecification/4",
            rated_power_hp=543,
            separator_type="Rotary",
            grain_tank_capacity_liters=15900,
            unloading_rate_liters_per_sec=177,
            compatible_header_types="Grain Platform, Folding Corn Head, Draper Platform",
            compatible_header_widths_m="10.7, 12.2, 13.7, 15.2",
            standard_features="AFS Pro 1200 Display, Adaptive Ground Speed System, AFS Harvest Command Automation, CrossFlow Cleaning System",
            optional_features="AFS Soil Command, Extended Wear Package, Residue Management System",
            production_start_date="2023-06-01",
            msrp_base_usd=565000.00
        ),
    ]
    
    for model in models:
        try:
            client.insert_document(model, commit_msg=f"Add combine model {model.model_name}")
            print(f"  ✓ Added {model.manufacturer} {model.model_name}")
        except Exception as e:
            print(f"  ! {model.model_name}: {e}")


def load_baler_models(client):
    """Load baler model configurations"""
    print("\nLoading baler models...")
    
    models = [
        RoundBalerModel(
            manufacturer="John Deere",
            model_name="569 Premium",
            model_year=2024,
            baler_type="Round",
            pto_hp_required_min=75,
            pto_hp_required_recommended=100,
            pto_speed_rpm=540,
            bale_weight_capacity_kg=726,
            bales_per_hour_typical=35,
            bales_per_hour_max=50,
            chamber_type="Variable",
            bale_diameter_min_cm=91,
            bale_diameter_max_cm=152,
            bale_width_cm=122,
            twine_systems="MaxiWrap Plus, CoverEdge Net Wrap",
            standard_features="MegaWide Plus Pickup, CoverEdge Net Wrap System, B-Wrap Monitor",
            optional_features="Bale Command Plus, Pre-Cutter System, Preservative Applicator",
            production_start_date="2023-01-01",
            msrp_base_usd=55000.00
        ),
        SquareBalerModel(
            manufacturer="Case IH",
            model_name="LB436",
            model_year=2024,
            baler_type="Large Square",
            pto_hp_required_min=120,
            pto_hp_required_recommended=140,
            pto_speed_rpm=1000,
            bale_weight_capacity_kg=544,
            bales_per_hour_typical=25,
            bales_per_hour_max=35,
            bale_width_cm=91,
            bale_height_cm=91,
            bale_length_cm=244,
            bale_density_kg_per_m3=200,
            compression_type="Packer Crank",
            twine_systems="4-Tie Knotter System",
            standard_features="AFS Pro 700 Display, Packer Crank Density Control, XtraTie Option",
            optional_features="Bale Ramp, Preservative System, Wide Pickup",
            production_start_date="2023-04-01",
            msrp_base_usd=145000.00
        ),
    ]
    
    for model in models:
        try:
            client.insert_document(model, commit_msg=f"Add baler model {model.model_name}")
            print(f"  ✓ Added {model.manufacturer} {model.model_name}")
        except Exception as e:
            print(f"  ! {model.model_name}: {e}")


def load_construction_models(client):
    """Load construction equipment model configurations"""
    print("\nLoading construction equipment models...")
    
    models = [
        ConstructionEquipmentModel(
            manufacturer="Caterpillar",
            model_name="320 Excavator",
            model_year=2024,
            equipment_category="Excavator",
            size_class="Mid-Size",
            engine="EngineSpecification/3",
            rated_power_hp=158,
            operating_weight_kg=22600,
            bucket_capacity_m3=1.0,
            max_dig_depth_m=6.7,
            max_reach_m=9.9,
            standard_features="Cat Grade with 2D, Cat Product Link, Hydraulic Quick Coupler, ROPS/FOPS Cab",
            optional_features="Cat Grade with 3D, Advanced Hydraulic System, Thumb and Auxiliary Hydraulics, Air Conditioning Upgrade",
            available_attachments="General Purpose Buckets, Heavy Duty Buckets, Hydraulic Thumbs, Grapples, Hammers",
            production_start_date="2023-01-01",
            msrp_base_usd=185000.00
        ),
        ConstructionEquipmentModel(
            manufacturer="Caterpillar",
            model_name="D6T Dozer",
            model_year=2024,
            equipment_category="Dozer",
            size_class="Large",
            engine="EngineSpecification/2",
            rated_power_hp=270,
            operating_weight_kg=21400,
            blade_capacity_m3=3.5,
            standard_features="Differential Steering, Electronic Monitoring System, ROPS/FOPS Cab",
            optional_features="Cat Grade with Slope Indicate, Ripper, Winch Package",
            production_start_date="2023-01-01",
            msrp_base_usd=275000.00
        ),
    ]
    
    for model in models:
        try:
            client.insert_document(model, commit_msg=f"Add construction model {model.model_name}")
            print(f"  ✓ Added {model.manufacturer} {model.model_name}")
        except Exception as e:
            print(f"  ! {model.model_name}: {e}")


def load_all_model_catalog_data():
    """Load complete model catalog dataset"""
    print("\n" + "=" * 80)
    print("  LOADING EQUIPMENT MODEL CATALOG DATA")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Load in order of dependencies
    load_manufacturers(client)
    load_engine_specs(client)
    load_hydraulic_specs(client)
    load_dimension_specs(client)
    load_tractor_models(client)
    load_tractor_trims(client)
    load_combine_models(client)
    load_baler_models(client)
    load_construction_models(client)
    
    print("\n" + "=" * 80)
    print("  MODEL CATALOG DATA LOADED SUCCESSFULLY")
    print("=" * 80)
    print("\nThe catalog now contains:")
    print("  - 5 manufacturers")
    print("  - Multiple engine, hydraulic, and dimension specifications")
    print("  - 3 tractor models with 4 trim variants")
    print("  - 2 combine models")
    print("  - 2 baler models")
    print("  - 2 construction equipment models")
    print("\nThis represents a REFERENCE CATALOG of model configurations,")
    print("not individual equipment instances.")


if __name__ == "__main__":
    try:
        load_all_model_catalog_data()
    except Exception as e:
        print(f"\n✗ Error loading model catalog data: {e}")
        import traceback
        traceback.print_exc()
        raise
