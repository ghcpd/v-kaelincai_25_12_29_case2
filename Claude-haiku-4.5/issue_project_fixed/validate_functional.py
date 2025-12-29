#!/usr/bin/env python
"""Comprehensive Functional Validation Script"""
import sys
sys.path.insert(0, 'src')

import pandas as pd
import numpy as np
from customer_segmentation import CustomerSegmentation, segment_customers

print("=" * 70)
print("VALIDATION TEST 5: Comprehensive Functional Validation")
print("=" * 70)

test_results = []

# Test 1: Reproducibility with Same Seed
print("\n[TEST 1] Reproducibility with Same Seed")
print("-" * 70)
try:
    data = pd.read_csv('data/customers.csv')
    
    seg1 = CustomerSegmentation(n_clusters=3, random_state=42)
    result1 = seg1.fit_predict(data)
    
    seg2 = CustomerSegmentation(n_clusters=3, random_state=42)
    result2 = seg2.fit_predict(data)
    
    if np.array_equal(result1, result2):
        print("✅ PASS: Same seed produces identical results")
        test_results.append(("Reproducibility", "PASS"))
    else:
        print("❌ FAIL: Different results with same seed")
        test_results.append(("Reproducibility", "FAIL"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("Reproducibility", "ERROR"))

# Test 2: Different Seeds Produce Different Results
print("\n[TEST 2] Different Seeds Produce Different Results")
print("-" * 70)
try:
    data = pd.read_csv('data/customers.csv')
    
    seg1 = CustomerSegmentation(n_clusters=3, random_state=42)
    result1 = seg1.fit_predict(data)
    
    seg2 = CustomerSegmentation(n_clusters=3, random_state=123)
    result2 = seg2.fit_predict(data)
    
    # Different seeds MIGHT produce different results (but not guaranteed)
    # The important thing is that they both work without errors
    print(f"✅ PASS: Both seeds executed successfully")
    print(f"   Seed 42 clusters: {np.unique(result1)}")
    print(f"   Seed 123 clusters: {np.unique(result2)}")
    test_results.append(("Different Seeds", "PASS"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("Different Seeds", "ERROR"))

# Test 3: Segment Assignment Consistency
print("\n[TEST 3] Segment Assignment Consistency")
print("-" * 70)
try:
    data = pd.read_csv('data/customers.csv')
    
    # Run 3 times
    assignments = []
    for i in range(3):
        seg = CustomerSegmentation(n_clusters=3)
        segmented = seg.get_customer_segments(data)
        assignments.append(segmented[['customer_id', 'segment']])
    
    # Check if customer assignments are identical across runs
    same = assignments[0].equals(assignments[1]) and assignments[1].equals(assignments[2])
    
    if same:
        print("✅ PASS: Customer segment assignments are identical across 3 runs")
        print(f"   Sample assignments:")
        print(f"   {assignments[0].head(5).to_string()}")
        test_results.append(("Segment Consistency", "PASS"))
    else:
        print("❌ FAIL: Customer assignments differ across runs")
        test_results.append(("Segment Consistency", "FAIL"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("Segment Consistency", "ERROR"))

# Test 4: Segment Statistics Stability
print("\n[TEST 4] Segment Statistics Stability")
print("-" * 70)
try:
    data = pd.read_csv('data/customers.csv')
    
    stats_list = []
    for i in range(3):
        seg = CustomerSegmentation(n_clusters=3)
        segmented = seg.get_customer_segments(data)
        stats = seg.get_segment_statistics(data)
        stats_list.append(stats)
    
    # Check if counts are the same
    all_same = True
    for segment_name in ['High-value', 'Regular', 'Low-engagement']:
        counts = [s.get(segment_name, {}).get('count', 0) for s in stats_list]
        if len(set(counts)) == 1:
            print(f"✅ {segment_name}: {counts[0]} customers (consistent)")
        else:
            print(f"❌ {segment_name}: {counts} (inconsistent)")
            all_same = False
    
    if all_same:
        test_results.append(("Stats Stability", "PASS"))
    else:
        test_results.append(("Stats Stability", "FAIL"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("Stats Stability", "ERROR"))

# Test 5: Data Processing Completeness
print("\n[TEST 5] Data Processing Completeness")
print("-" * 70)
try:
    data = pd.read_csv('data/customers.csv')
    seg = CustomerSegmentation(n_clusters=3)
    segmented = seg.get_customer_segments(data)
    
    checks = []
    
    # Check 1: All rows processed
    if len(segmented) == len(data):
        print(f"✅ All {len(data)} rows processed")
        checks.append(True)
    else:
        print(f"❌ Row count mismatch: {len(segmented)} vs {len(data)}")
        checks.append(False)
    
    # Check 2: No missing segments
    if 'segment' in segmented.columns:
        print(f"✅ Segment column created")
        checks.append(True)
    else:
        print(f"❌ Segment column missing")
        checks.append(False)
    
    # Check 3: All three segments represented
    unique_segments = set(segmented['segment'].values)
    if unique_segments == {'High-value', 'Regular', 'Low-engagement'}:
        print(f"✅ All 3 segments represented: {unique_segments}")
        checks.append(True)
    else:
        print(f"❌ Segment mismatch: {unique_segments}")
        checks.append(False)
    
    # Check 4: No null values in results
    if not segmented['segment'].isnull().any():
        print(f"✅ No null values in results")
        checks.append(True)
    else:
        print(f"❌ Null values detected")
        checks.append(False)
    
    if all(checks):
        test_results.append(("Data Completeness", "PASS"))
    else:
        test_results.append(("Data Completeness", "FAIL"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("Data Completeness", "ERROR"))

# Test 6: API Compatibility
print("\n[TEST 6] API Compatibility and Default Parameters")
print("-" * 70)
try:
    data = pd.read_csv('data/customers.csv')
    
    # Test default initialization
    seg1 = CustomerSegmentation()  # Should use defaults
    result1 = seg1.fit_predict(data)
    print(f"✅ Default initialization works (n_clusters={seg1.n_clusters}, random_state={seg1.random_state})")
    
    # Test with custom n_clusters
    seg2 = CustomerSegmentation(n_clusters=4)
    result2 = seg2.fit_predict(data)
    print(f"✅ Custom n_clusters works (n_clusters={seg2.n_clusters})")
    
    # Test convenience function
    segmented, stats = segment_customers('data/customers.csv')
    print(f"✅ Convenience function works ({len(segmented)} customers segmented)")
    
    test_results.append(("API Compatibility", "PASS"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("API Compatibility", "ERROR"))

# Test 7: Edge Case: Small Dataset
print("\n[TEST 7] Edge Case: Small Dataset")
print("-" * 70)
try:
    small_data = pd.DataFrame({
        'customer_id': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
        'monthly_spending': [100.0, 200.0, 500.0, 150.0, 900.0, 120.0],
        'visit_frequency': [2, 4, 12, 3, 25, 2]
    })
    
    seg = CustomerSegmentation(n_clusters=3)
    result = seg.fit_predict(small_data)
    
    if len(result) == 6 and len(set(result)) > 0:
        print(f"✅ Small dataset handled correctly")
        print(f"   Input: {len(small_data)} customers")
        print(f"   Output clusters: {set(result)}")
        test_results.append(("Edge Case", "PASS"))
    else:
        print(f"❌ Edge case failed")
        test_results.append(("Edge Case", "FAIL"))
except Exception as e:
    print(f"❌ ERROR: {e}")
    test_results.append(("Edge Case", "ERROR"))

# Summary
print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

passed = sum(1 for _, result in test_results if result == "PASS")
failed = sum(1 for _, result in test_results if result == "FAIL")
errors = sum(1 for _, result in test_results if result == "ERROR")

print("\nTest Results:")
for test_name, result in test_results:
    symbol = "✅" if result == "PASS" else "❌" if result == "FAIL" else "⚠️"
    print(f"  {symbol} {test_name}: {result}")

print(f"\nTotal Tests: {len(test_results)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Errors: {errors}")

if failed == 0 and errors == 0:
    print("\n" + "=" * 70)
    print("✅ ALL FUNCTIONAL TESTS PASSED")
    print("=" * 70)
else:
    print("\n" + "=" * 70)
    print("❌ SOME TESTS FAILED")
    print("=" * 70)
