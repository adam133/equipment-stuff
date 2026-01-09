"""
Demonstrate how TerminusDB handles schema changes and existing data

This script shows:
1. What happens to existing data when schema is updated
2. Different strategies for schema evolution
"""

from init_db import get_client, DB_NAME
from schema import SmallSquareBaler, LargeSquareBaler, RoundBaler

def demonstrate_schema_evolution():
    """Demonstrate schema evolution behavior"""
    print("\n" + "=" * 80)
    print("  TERMINUSDB SCHEMA EVOLUTION DEMONSTRATION")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Query the new baler classes
    print("\n1. VERIFYING NEW SCHEMA CLASSES")
    print("-" * 80)
    
    small_square_balers = list(client.get_all_documents(
        graph_type="instance", 
        document_template=SmallSquareBaler
    ))
    print(f"\nSmall Square Balers: {len(small_square_balers)}")
    for baler in small_square_balers:
        print(f"  - {baler.get('model')} ({baler.get('year')})")
        print(f"    Bale size: {baler.get('bale_width')}\" x {baler.get('bale_height')}\" x {baler.get('bale_length')}\"")
        print(f"    Capacity: {baler.get('bales_per_hour')} bales/hour")
    
    large_square_balers = list(client.get_all_documents(
        graph_type="instance",
        document_template=LargeSquareBaler
    ))
    print(f"\nLarge Square Balers: {len(large_square_balers)}")
    for baler in large_square_balers:
        print(f"  - {baler.get('model')} ({baler.get('year')})")
        print(f"    Bale size: {baler.get('bale_width')}\" x {baler.get('bale_height')}\" x {baler.get('bale_length')}\"")
        print(f"    Density: {baler.get('bale_density')}")
    
    round_balers = list(client.get_all_documents(
        graph_type="instance",
        document_template=RoundBaler
    ))
    print(f"\nRound Balers: {len(round_balers)}")
    for baler in round_balers:
        print(f"  - {baler.get('model')} ({baler.get('year')})")
        print(f"    Bale size: {baler.get('bale_diameter')}\" diameter x {baler.get('bale_width')}\" wide")
        print(f"    Chamber: {baler.get('chamber_type')}")
    
    # Show all equipment types
    print("\n2. ALL EQUIPMENT IN DATABASE")
    print("-" * 80)
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    equipment_by_type = {}
    
    for doc in all_docs:
        doc_type = doc.get('@type')
        if doc_type != 'Manufacturer':
            equipment_by_type[doc_type] = equipment_by_type.get(doc_type, 0) + 1
    
    print("\nEquipment counts by type:")
    for eq_type, count in sorted(equipment_by_type.items()):
        print(f"  - {eq_type}: {count}")
    
    print("\n" + "=" * 80)
    print("  KEY INSIGHTS ABOUT SCHEMA EVOLUTION IN TERMINUSDB")
    print("=" * 80)
    
    print("""
1. ADDING NEW CLASSES (like Baler subclasses):
   - New classes can be added without affecting existing data
   - Existing documents remain intact and accessible
   - New documents can use the new schema classes immediately
   - This is a NON-BREAKING change

2. MODIFYING EXISTING CLASSES:
   - Adding optional fields: Safe, existing data remains valid
   - Adding required fields: Need to handle existing data (migration)
   - Removing fields: Existing data keeps the field but schema won't validate it
   - Changing field types: May require data migration

3. DATA PRESERVATION:
   - TerminusDB maintains schema history through commits
   - Data is versioned along with schema changes
   - Can query historical versions if needed

4. STRATEGIES FOR SCHEMA EVOLUTION:
   
   a) DEVELOPMENT (current approach):
      - Delete and recreate database for clean slate
      - Fast iteration during development
      - No migration needed
   
   b) PRODUCTION:
      - Incremental schema updates using schema.commit()
      - Write migration scripts for breaking changes
      - Test migrations on copies before production
      - Use optional fields when possible to avoid breaking changes
   
   c) BACKWARDS COMPATIBILITY:
      - Add new classes instead of modifying existing ones
      - Use optional fields for new attributes
      - Deprecate rather than remove
      - Version your schema classes if needed

5. CURRENT DEMONSTRATION:
   - Added 3 new baler classes (SmallSquareBaler, LargeSquareBaler, RoundBaler)
   - Loaded sample data into new classes
   - Existing Tractor, Combine, and ConstructionEquipment data unchanged
   - All equipment types coexist in the same database
    """)
    
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        demonstrate_schema_evolution()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
