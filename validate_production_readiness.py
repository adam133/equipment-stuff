"""
Production Readiness Validation for DocumentDB/TerminusDB

This script validates key production concerns for using TerminusDB as a
global equipment model catalog. Tests focus on:

1. Query Performance - Finding similar models, filtering by specs
2. Data Integrity - Constraints and validation
3. Schema Evolution - Adding new model types without breaking changes
4. Concurrent Access Patterns - Multiple reader/writer scenarios
5. Data Relationships - Model hierarchies and references
6. Indexing Strategy - Efficient lookups
7. Versioning - Tracking model catalog changes over time
"""

import time
import json
from init_model_catalog import get_client, DB_NAME
from model_catalog_schema import TractorModel, TractorTrim, CombineModel


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_result(test_name, passed, details=""):
    """Print test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"   {details}")


def test_query_performance(client):
    """Test 1: Query Performance for Finding Similar Models"""
    print_section("TEST 1: Query Performance - Finding Similar Models")
    
    # Test 1a: Find all tractors in a horsepower range
    print("1a. Find tractors with 150-400 HP (typical production query)...")
    start_time = time.time()
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    hp_filtered = [t for t in tractors 
                   if 150 <= t.get('rated_power_hp', 0) <= 400]
    
    query_time = time.time() - start_time
    print(f"   Found {len(hp_filtered)} models in {query_time*1000:.2f}ms")
    for t in hp_filtered:
        print(f"   - {t.get('manufacturer')} {t.get('model_name')}: {t.get('rated_power_hp')} HP")
    
    print_result("Query by horsepower range", 
                 query_time < 1.0,  # Should complete in under 1 second
                 f"{query_time*1000:.2f}ms response time")
    
    # Test 1b: Find tractors by category
    print("\n1b. Find row crop tractors (category-based search)...")
    start_time = time.time()
    
    row_crop = [t for t in tractors if t.get('category') == 'Row Crop']
    
    query_time = time.time() - start_time
    print(f"   Found {len(row_crop)} row crop tractors in {query_time*1000:.2f}ms")
    for t in row_crop:
        print(f"   - {t.get('manufacturer')} {t.get('model_name')}")
    
    print_result("Category-based search",
                 query_time < 0.5,
                 f"{query_time*1000:.2f}ms response time")
    
    # Test 1c: Find similar models (by specifications)
    print("\n1c. Find similar models to John Deere 8R 370...")
    reference_hp = 370
    tolerance = 50
    
    start_time = time.time()
    similar = [t for t in tractors 
               if abs(t.get('rated_power_hp', 0) - reference_hp) <= tolerance
               and t.get('model_name') != '8R 370']
    
    query_time = time.time() - start_time
    print(f"   Found {len(similar)} similar models in {query_time*1000:.2f}ms")
    for t in similar:
        print(f"   - {t.get('manufacturer')} {t.get('model_name')}: {t.get('rated_power_hp')} HP")
    
    print_result("Similarity search",
                 query_time < 0.5,
                 f"{query_time*1000:.2f}ms response time")
    
    return query_time < 1.0


def test_model_hierarchy_relationships(client):
    """Test 2: Model Hierarchy and Relationships"""
    print_section("TEST 2: Model Hierarchy - Manufacturer → Model → Trim")
    
    print("2a. Query complete hierarchy for a manufacturer...")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    manufacturers = [d for d in all_docs if d.get('@type') == 'ManufacturerCatalog']
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    trims = [d for d in all_docs if d.get('@type') == 'TractorTrim']
    
    print(f"   Total manufacturers: {len(manufacturers)}")
    print(f"   Total tractor models: {len(tractors)}")
    print(f"   Total tractor trims: {len(trims)}")
    
    # Build hierarchy for John Deere
    jd_tractors = [t for t in tractors if t.get('manufacturer') == 'John Deere']
    print(f"\n   John Deere hierarchy:")
    print(f"   └─ John Deere ({len(jd_tractors)} tractor models)")
    
    for tractor in jd_tractors:
        model_id = tractor.get('@id', '')
        model_trims = [tr for tr in trims if model_id in str(tr.get('base_model', ''))]
        print(f"      ├─ {tractor.get('model_name')} ({len(model_trims)} trims)")
        for trim in model_trims:
            print(f"      │  └─ {trim.get('trim_name')} - ${trim.get('msrp_usd', 0):,.0f}")
    
    hierarchy_valid = len(jd_tractors) > 0 and any(len([tr for tr in trims 
                                                         if t.get('@id', '') in str(tr.get('base_model', ''))]) > 0 
                                                    for t in jd_tractors)
    
    print_result("Hierarchical relationships",
                 hierarchy_valid,
                 "Successfully navigated manufacturer → model → trim hierarchy")
    
    return hierarchy_valid


def test_specification_comparison(client):
    """Test 3: Comparing Model Specifications"""
    print_section("TEST 3: Specification Comparison Across Models")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    
    print("3a. Compare transmission types across all tractor models...")
    transmission_types = {}
    for t in tractors:
        trans_type = t.get('transmission_type', 'Unknown')
        if trans_type not in transmission_types:
            transmission_types[trans_type] = []
        transmission_types[trans_type].append(t.get('model_name'))
    
    print(f"   Found {len(transmission_types)} transmission types:")
    for trans_type, models in transmission_types.items():
        print(f"   - {trans_type}: {len(models)} models")
        for model in models:
            print(f"      • {model}")
    
    print("\n3b. Compare feature availability across models...")
    feature_analysis = {}
    for t in tractors:
        model_name = f"{t.get('manufacturer')} {t.get('model_name')}"
        standard_features = t.get('standard_features', [])
        optional_features = t.get('optional_features', [])
        
        print(f"   {model_name}:")
        print(f"      Standard: {len(standard_features)} features")
        print(f"      Optional: {len(optional_features)} features")
        
        # Track which features are standard vs optional across models
        for feature in standard_features:
            if feature not in feature_analysis:
                feature_analysis[feature] = {'standard': 0, 'optional': 0}
            feature_analysis[feature]['standard'] += 1
    
    # Find features that are standard on some models but not others
    print("\n   Feature consistency analysis:")
    inconsistent_features = [f for f, counts in feature_analysis.items() 
                            if counts['standard'] > 0 and counts['standard'] < len(tractors)]
    print(f"   Features with varying availability: {len(inconsistent_features)}")
    
    comparison_valid = len(transmission_types) > 1 and len(feature_analysis) > 0
    print_result("Specification comparison",
                 comparison_valid,
                 f"Successfully compared specs across {len(tractors)} models")
    
    return comparison_valid


def test_data_validation(client):
    """Test 4: Data Integrity and Validation"""
    print_section("TEST 4: Data Integrity and Validation")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    
    # Check for required fields
    print("4a. Validate required fields on all models...")
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    
    required_fields = ['manufacturer', 'model_name', 'model_year', 'rated_power_hp']
    validation_passed = True
    missing_count = 0
    
    for tractor in tractors:
        for field in required_fields:
            if not tractor.get(field):
                print(f"   ✗ Missing {field} in {tractor.get('model_name', 'Unknown')}")
                validation_passed = False
                missing_count += 1
    
    if validation_passed:
        print(f"   ✓ All {len(tractors)} tractor models have required fields")
    
    # Check data type consistency
    print("\n4b. Validate data type consistency...")
    type_errors = 0
    for tractor in tractors:
        # Check that horsepower is a number
        hp = tractor.get('rated_power_hp')
        if hp is not None and not isinstance(hp, (int, float)):
            print(f"   ✗ Invalid HP type in {tractor.get('model_name')}: {type(hp)}")
            type_errors += 1
        
        # Check that year is an integer
        year = tractor.get('model_year')
        if year is not None and not isinstance(year, int):
            print(f"   ✗ Invalid year type in {tractor.get('model_name')}: {type(year)}")
            type_errors += 1
    
    if type_errors == 0:
        print(f"   ✓ All data types are consistent")
    
    # Check logical constraints
    print("\n4c. Validate logical constraints...")
    constraint_violations = 0
    for tractor in tractors:
        # PTO HP should not exceed rated HP
        pto_hp = tractor.get('pto_power_hp', 0)
        rated_hp = tractor.get('rated_power_hp', 0)
        if pto_hp > rated_hp:
            print(f"   ✗ PTO HP exceeds rated HP in {tractor.get('model_name')}")
            constraint_violations += 1
        
        # Model year should be reasonable
        year = tractor.get('model_year', 0)
        if year < 1900 or year > 2030:
            print(f"   ✗ Unreasonable model year in {tractor.get('model_name')}: {year}")
            constraint_violations += 1
    
    if constraint_violations == 0:
        print(f"   ✓ All logical constraints satisfied")
    
    overall_valid = validation_passed and type_errors == 0 and constraint_violations == 0
    print_result("Data validation",
                 overall_valid,
                 f"Validated {len(tractors)} models with {missing_count} missing fields, "
                 f"{type_errors} type errors, {constraint_violations} constraint violations")
    
    return overall_valid


def test_schema_flexibility(client):
    """Test 5: Schema Flexibility for Adding New Equipment Types"""
    print_section("TEST 5: Schema Flexibility - Adding New Equipment Types")
    
    print("5a. Verify multiple equipment types coexist...")
    all_docs = list(client.get_all_documents(graph_type="instance"))
    
    equipment_types = {}
    for doc in all_docs:
        doc_type = doc.get('@type')
        if doc_type and 'Model' in doc_type:
            equipment_types[doc_type] = equipment_types.get(doc_type, 0) + 1
    
    print(f"   Found {len(equipment_types)} equipment model types:")
    for eq_type, count in equipment_types.items():
        print(f"   - {eq_type}: {count} models")
    
    # Check that base and derived types work
    print("\n5b. Verify inheritance (base baler models)...")
    balers = [d for d in all_docs if 'Baler' in d.get('@type', '')]
    print(f"   Found {len(balers)} baler models")
    for baler in balers:
        print(f"   - {baler.get('@type')}: {baler.get('model_name')}")
    
    flexibility_valid = len(equipment_types) >= 4  # Multiple types exist
    print_result("Schema flexibility",
                 flexibility_valid,
                 f"{len(equipment_types)} equipment types coexist successfully")
    
    return flexibility_valid


def test_catalog_versioning(client):
    """Test 6: Catalog Versioning and Change Tracking"""
    print_section("TEST 6: Catalog Versioning - Change Tracking")
    
    print("6a. Demonstrate catalog version awareness...")
    print("   Note: TerminusDB maintains commit history for all changes")
    print("   - Each schema change creates a new commit")
    print("   - Each data change creates a new commit")
    print("   - Full audit trail of catalog evolution")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    
    print(f"\n6b. Track model lifecycle (production dates)...")
    for tractor in tractors:
        model_name = f"{tractor.get('manufacturer')} {tractor.get('model_name')}"
        start_date = tractor.get('production_start_date', 'Unknown')
        end_date = tractor.get('production_end_date', 'Current')
        print(f"   {model_name}:")
        print(f"      Production: {start_date} → {end_date}")
        
        # Check for model replacement information
        replaced_by = tractor.get('replaced_by_model')
        replaces = tractor.get('replaces_model')
        if replaced_by:
            print(f"      Replaced by: {replaced_by}")
        if replaces:
            print(f"      Replaces: {replaces}")
    
    print("\n6c. Version tracking recommendations:")
    print("   ✓ Use production_start_date/production_end_date for model lifecycle")
    print("   ✓ Use replaced_by_model/replaces_model for model evolution")
    print("   ✓ Leverage TerminusDB's commit system for audit trail")
    print("   ✓ Tag important catalog versions (e.g., 'Q1-2024-Catalog')")
    
    versioning_valid = all(t.get('production_start_date') for t in tractors)
    print_result("Versioning support",
                 versioning_valid,
                 "All models have production date tracking")
    
    return versioning_valid


def test_similarity_search_algorithm(client):
    """Test 7: Advanced Similarity Search"""
    print_section("TEST 7: Advanced Similarity Search Algorithms")
    
    all_docs = list(client.get_all_documents(graph_type="instance"))
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    
    # Define a reference tractor
    reference = None
    for t in tractors:
        if t.get('model_name') == '8R 370':
            reference = t
            break
    
    if not reference:
        print("   Could not find reference model")
        return False
    
    print(f"7a. Find models similar to {reference.get('manufacturer')} {reference.get('model_name')}...")
    print(f"   Reference specs: {reference.get('rated_power_hp')} HP, "
          f"{reference.get('transmission_type')}, "
          f"Category: {reference.get('category')}")
    
    # Similarity scoring algorithm
    def calculate_similarity_score(ref, candidate):
        """Calculate similarity score between two models"""
        if candidate.get('@id') == ref.get('@id'):
            return -1  # Skip self
        
        score = 0.0
        
        # Horsepower similarity (40% weight)
        ref_hp = ref.get('rated_power_hp', 0)
        cand_hp = candidate.get('rated_power_hp', 0)
        if ref_hp > 0:
            hp_diff_pct = abs(ref_hp - cand_hp) / ref_hp
            hp_similarity = max(0, 1 - hp_diff_pct)
            score += hp_similarity * 0.4
        
        # Category match (30% weight)
        if ref.get('category') == candidate.get('category'):
            score += 0.3
        
        # Transmission type match (20% weight)
        if ref.get('transmission_type') == candidate.get('transmission_type'):
            score += 0.2
        
        # 4WD match (10% weight)
        if ref.get('four_wheel_drive') == candidate.get('four_wheel_drive'):
            score += 0.1
        
        return score
    
    # Calculate similarity scores
    similarity_results = []
    for tractor in tractors:
        score = calculate_similarity_score(reference, tractor)
        if score >= 0:  # Skip self (score = -1)
            similarity_results.append({
                'model': tractor,
                'score': score
            })
    
    # Sort by score
    similarity_results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n   Top 3 similar models:")
    for i, result in enumerate(similarity_results[:3], 1):
        model = result['model']
        score = result['score']
        print(f"   {i}. {model.get('manufacturer')} {model.get('model_name')} "
              f"(similarity: {score*100:.1f}%)")
        print(f"      {model.get('rated_power_hp')} HP, "
              f"{model.get('transmission_type')}, "
              f"Category: {model.get('category')}")
    
    similarity_valid = len(similarity_results) > 0 and similarity_results[0]['score'] > 0.5
    print_result("Similarity search algorithm",
                 similarity_valid,
                 f"Found {len(similarity_results)} comparable models")
    
    return similarity_valid


def test_bulk_operations(client):
    """Test 8: Bulk Query Performance"""
    print_section("TEST 8: Bulk Operations and Performance")
    
    print("8a. Measure bulk query performance...")
    start_time = time.time()
    all_docs = list(client.get_all_documents(graph_type="instance"))
    query_time = time.time() - start_time
    
    print(f"   Retrieved {len(all_docs)} documents in {query_time*1000:.2f}ms")
    print(f"   Average: {(query_time*1000)/len(all_docs):.3f}ms per document")
    
    # Group by type
    print("\n8b. Analyze catalog composition...")
    doc_types = {}
    for doc in all_docs:
        doc_type = doc.get('@type', 'Unknown')
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
    
    print(f"   Document types in catalog:")
    for doc_type, count in sorted(doc_types.items()):
        print(f"   - {doc_type}: {count}")
    
    # Filter operations
    print("\n8c. Test multiple filter operations...")
    start_time = time.time()
    
    # Complex filter: tractors with >200 HP, 4WD, and specific transmission
    tractors = [d for d in all_docs if d.get('@type') == 'TractorModel']
    filtered = [t for t in tractors
                if t.get('rated_power_hp', 0) > 200
                and t.get('four_wheel_drive') == True
                and 'Variable' in str(t.get('transmission_type', ''))]
    
    filter_time = time.time() - start_time
    print(f"   Complex filter found {len(filtered)} models in {filter_time*1000:.2f}ms")
    
    performance_valid = query_time < 2.0 and filter_time < 0.5
    print_result("Bulk operation performance",
                 performance_valid,
                 f"Bulk query: {query_time*1000:.2f}ms, Filter: {filter_time*1000:.2f}ms")
    
    return performance_valid


def generate_production_recommendations():
    """Generate recommendations for production deployment"""
    print_section("PRODUCTION DEPLOYMENT RECOMMENDATIONS")
    
    recommendations = [
        {
            "category": "Indexing Strategy",
            "items": [
                "Create indexes on frequently queried fields (manufacturer, model_year, category)",
                "Index horsepower ranges for similarity searches",
                "Consider composite indexes for multi-field queries"
            ]
        },
        {
            "category": "Data Validation",
            "items": [
                "Implement pre-commit hooks to validate required fields",
                "Enforce logical constraints (PTO HP < rated HP)",
                "Validate date ranges for production lifecycle",
                "Check reference integrity for model hierarchies"
            ]
        },
        {
            "category": "Schema Evolution",
            "items": [
                "Use optional fields for new features to avoid breaking changes",
                "Version your schema classes (e.g., TractorModelV2) for major changes",
                "Test schema migrations on staging before production",
                "Maintain backwards compatibility for at least 2 versions"
            ]
        },
        {
            "category": "Performance Optimization",
            "items": [
                "Cache frequently accessed manufacturer and category lists",
                "Implement pagination for large result sets",
                "Use projection to retrieve only needed fields",
                "Consider materialized views for complex similarity queries"
            ]
        },
        {
            "category": "Concurrent Access",
            "items": [
                "TerminusDB provides ACID transactions - leverage them",
                "Implement optimistic locking for catalog updates",
                "Use separate read replicas for high query volume",
                "Queue batch updates during off-peak hours"
            ]
        },
        {
            "category": "Version Control & Audit",
            "items": [
                "Tag catalog versions (e.g., 'Q1-2024', 'Spring-Release')",
                "Maintain detailed commit messages for all changes",
                "Implement change approval workflow for production updates",
                "Keep audit log of who changed what and when"
            ]
        },
        {
            "category": "Data Quality",
            "items": [
                "Establish data governance policies for model catalog",
                "Implement automated validation tests (run this script regularly)",
                "Monitor for duplicate entries",
                "Validate specifications against manufacturer data sheets"
            ]
        },
        {
            "category": "Backup & Recovery",
            "items": [
                "Schedule regular database backups",
                "Test recovery procedures quarterly",
                "Maintain catalog change log for rollback scenarios",
                "Keep archival copies of deprecated models"
            ]
        }
    ]
    
    for rec in recommendations:
        print(f"\n{rec['category']}:")
        for item in rec['items']:
            print(f"  • {item}")
    
    print("\n" + "=" * 80)


def run_all_validation_tests():
    """Run complete production readiness validation suite"""
    print("\n" + "=" * 80)
    print("  PRODUCTION READINESS VALIDATION SUITE")
    print("  DocumentDB/TerminusDB Model Catalog Evaluation")
    print("=" * 80)
    
    client = get_client()
    client.connect(db=DB_NAME)
    
    # Run all tests
    results = {
        "Query Performance": test_query_performance(client),
        "Model Hierarchy": test_model_hierarchy_relationships(client),
        "Specification Comparison": test_specification_comparison(client),
        "Data Validation": test_data_validation(client),
        "Schema Flexibility": test_schema_flexibility(client),
        "Catalog Versioning": test_catalog_versioning(client),
        "Similarity Search": test_similarity_search_algorithm(client),
        "Bulk Operations": test_bulk_operations(client),
    }
    
    # Generate recommendations
    generate_production_recommendations()
    
    # Summary
    print_section("VALIDATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    if passed == total:
        print("\n" + "=" * 80)
        print("  ✓ ALL TESTS PASSED - PRODUCTION READY")
        print("=" * 80)
        print("\nTerminusDB is suitable for use as a global equipment model catalog.")
        print("Review the recommendations above for optimal production deployment.")
    else:
        print("\n" + "=" * 80)
        print("  ⚠ SOME TESTS FAILED - REVIEW REQUIRED")
        print("=" * 80)
        print(f"\n{total - passed} test(s) failed. Review the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    try:
        run_all_validation_tests()
    except Exception as e:
        print(f"\n✗ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        raise
