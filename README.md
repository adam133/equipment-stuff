# Equipment Database - TerminusDB Proof of Concept

A proof of concept using TerminusDB for managing an equipment database that tracks tractors, combines, and construction equipment. This project demonstrates schema design, data loading, querying, and update operations with TerminusDB.

## Features

- **Comprehensive Schema**: Supports multiple equipment types (tractors, combines, construction equipment, balers) with type-specific attributes
- **Manufacturer Tracking**: Maintains manufacturer information with relationships to equipment
- **Rich Metadata**: Tracks equipment condition, hours used, location, values, and more
- **Sample Data**: Includes realistic sample data for demonstration
- **Query Examples**: Demonstrates various query patterns for filtering and aggregating data
- **CRUD Operations**: Examples for adding, updating, and managing equipment records

## Equipment Types

### Tractors
- Horsepower, transmission type, PTO HP
- Lift capacity, 4WD capability
- Examples: John Deere 8R 370, Kubota M7-152, Case IH Magnum 340

### Combines
- Header width, grain tank capacity
- Separator type (Conventional, Rotary, Hybrid)
- Examples: John Deere S780, New Holland CR8.90

### Construction Equipment
- Operating weight, digging depth, reach
- Bucket capacity, lift capacity
- Types: Excavators, Bulldozers, Backhoes, Cranes/Telehandlers

### Balers
- PTO horsepower requirements, bale weight capacity
- Bale dimensions (width, height, length, diameter)
- Bales per hour capacity
- Types: Small Square Balers, Large Square Balers, Round Balers
- Examples: New Holland BC5060, Case IH LB436, John Deere 569 Premium

## Prerequisites

- Docker and Docker Compose (for running TerminusDB server)
- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

### 1. Start TerminusDB Server

Start the TerminusDB server using Docker Compose:

```bash
docker compose up -d
```

This will:
- Start TerminusDB on `http://localhost:6363`
- Set up the admin password as `root`
- Create a persistent volume for data storage

Wait a few seconds for the server to fully start up.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

Create the database and set up the schema:

```bash
python init_db.py
```

This creates a new database called `equipment_db`.

### 4. Load Sample Data

Populate the database with sample equipment:

```bash
python load_data.py
```

This loads:
- 5 manufacturers (John Deere, Case IH, Caterpillar, Kubota, New Holland)
- 3 tractors
- 2 combines
- 4 construction equipment items
- 6 balers (2 small square, 2 large square, 2 round)

### 5. Run Query Examples

See various ways to query the data:

```bash
python query_examples.py
```

This demonstrates:
- Querying all equipment by type
- Filtering by manufacturer
- Filtering by condition
- Finding high-value equipment
- Finding low-hours equipment
- Searching by location
- Finding recent equipment
- Getting summary statistics

### 6. Run Add/Update Examples

See how to add and update equipment:

```bash
python update_examples.py
```

This demonstrates:
- Adding new manufacturers
- Adding new equipment (tractors, combines, construction)
- Updating equipment hours
- Updating equipment condition
- Updating equipment location
- Updating equipment values

## Project Structure

```
equipment-stuff/
├── docker-compose.yml      # TerminusDB server configuration
├── requirements.txt        # Python dependencies
├── schema.py              # Database schema definitions
├── init_db.py             # Database initialization script
├── load_data.py           # Sample data loading script
├── query_examples.py      # Query demonstrations
├── update_examples.py     # Add/Update demonstrations
└── README.md              # This file
```

## Schema Design

The database uses a hierarchical schema:

```
Manufacturer
    ↓
Equipment (base class)
    ├── Tractor
    ├── Combine
    ├── ConstructionEquipment
    └── Balers
        ├── SmallSquareBaler
        ├── LargeSquareBaler
        └── RoundBaler
```

### Core Fields (All Equipment)
- `serial_number`: Unique identifier
- `equipment_type`: Enum (tractor, combine, excavator, etc.)
- `manufacturer`: Reference to Manufacturer
- `model`: Model name/number
- `year`: Manufacturing year
- `condition`: Enum (excellent, good, fair, poor, needs_repair)
- `purchase_price`: Original purchase price
- `current_value`: Current estimated value
- `hours_used`: Total hours of operation
- `location`: Current storage/usage location
- `notes`: Additional notes

### Type-Specific Fields

**Tractors:**
- `horsepower`, `transmission_type`, `pto_hp`
- `lift_capacity`, `four_wheel_drive`

**Combines:**
- `header_width`, `grain_tank_capacity`
- `horsepower`, `separator_type`

**Construction Equipment:**
- `operating_weight`, `max_digging_depth`
- `max_reach`, `bucket_capacity`, `max_lift_capacity`

**Balers (All Types):**
- `pto_hp_required`, `bale_weight_capacity`

**Small Square Balers:**
- `bale_width`, `bale_height`, `bale_length`
- `bales_per_hour`

**Large Square Balers:**
- `bale_width`, `bale_height`, `bale_length`
- `bales_per_hour`, `bale_density`

**Round Balers:**
- `bale_diameter`, `bale_width`
- `bales_per_hour`, `chamber_type`

## How TerminusDB Handles Schema Changes

TerminusDB manages schema evolution through its commit-based system:

### Schema Definition
- Schemas are defined using `WOQLSchema()` and `DocumentTemplate` classes
- Each document type is defined declaratively with typed fields
- The schema is stored as part of the database

### Schema Commits
- Schema changes are committed using `schema.commit(client, commit_msg="...")`
- Each schema change creates a new commit in the database history
- This allows tracking of schema evolution over time

### Schema Updates
- To modify the schema, update the `schema.py` file with new classes or fields
- Re-run `init_db.py` to delete and recreate the database with the new schema
- Alternatively, for production systems, you can perform incremental schema updates

### Adding New Equipment Types
This project demonstrates schema extension by adding the Baler class hierarchy:
1. Define base `Baler` class with common attributes
2. Define subclasses (`SmallSquareBaler`, `LargeSquareBaler`, `RoundBaler`) with specific attributes
3. Commit the updated schema to TerminusDB
4. Load sample data using the new classes

## Usage Examples

### Querying Equipment

```python
from init_db import get_client, DB_NAME
from schema import Tractor

client = get_client()
client.connect(db=DB_NAME)

# Get all tractors
tractors = client.get_all_documents(graph_type="instance", document_template=Tractor)

# Filter and display
for tractor in tractors:
    print(f"{tractor['model']} - {tractor['hours_used']} hours")
```

### Adding New Equipment

```python
from schema import Tractor, EquipmentType, EquipmentCondition

new_tractor = Tractor(
    serial_number="ABC-123-2023-001",
    equipment_type=EquipmentType.tractor,
    manufacturer="Manufacturer/John Deere",
    model="6M Series",
    year=2023,
    condition=EquipmentCondition.excellent,
    horsepower=145,
    transmission_type="Automatic",
    four_wheel_drive=True
)

client.insert_document(new_tractor, commit_msg="Add new tractor")
```

### Updating Equipment

```python
# Get equipment
equipment = client.get_all_documents(graph_type="instance", document_template=Tractor)
tractor = equipment[0]

# Update hours
tractor['hours_used'] = 1500

# Save changes
client.replace_document(tractor, commit_msg="Update tractor hours")
```

## Stopping the Database

To stop the TerminusDB server:

```bash
docker compose down
```

To stop and remove all data:

```bash
docker compose down -v
```

## Troubleshooting

### TerminusDB not connecting
- Ensure Docker is running
- Check that port 6363 is not in use
- Wait a few seconds after `docker compose up` for the server to start
- Check logs: `docker compose logs terminusdb`

### Python dependencies error
- Ensure you're using Python 3.8+
- Try upgrading pip: `pip install --upgrade pip`
- Use a virtual environment for clean installation

### Database already exists error
- The `init_db.py` script will delete and recreate the database
- Alternatively, use TerminusDB console at `http://localhost:6363` to manage databases

## Next Steps

This proof of concept can be extended with:

1. **Web Interface**: Add a Flask/FastAPI frontend for equipment management
2. **Maintenance Tracking**: Add maintenance records and schedules
3. **Cost Analysis**: Track operating costs, fuel usage, repairs
4. **Depreciation Calculations**: Automatic value depreciation over time
5. **Parts Inventory**: Link equipment to spare parts and supplies
6. **User Management**: Multi-user access with permissions
7. **Reports**: Generate PDF reports on equipment fleet
8. **API**: RESTful API for external system integration

## Resources

- [TerminusDB Documentation](https://terminusdb.com/docs/)
- [TerminusDB Python Client](https://github.com/terminusdb/terminusdb-client-python)
- [TerminusDB Console](http://localhost:6363) (when running)

## License

This is a proof of concept project for demonstration purposes.