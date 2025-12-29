#!/usr/bin/env python
"""System Launch and Import Validation Script"""
import sys
sys.path.insert(0, 'src')

print("=" * 60)
print("VALIDATION TEST 3: System Launch and Imports")
print("=" * 60)

try:
    print("\n[1] Importing modules...")
    from customer_segmentation import CustomerSegmentation, segment_customers
    import pandas as pd
    print("    ✅ Module imported successfully")
    
    print("\n[2] Initializing CustomerSegmentation...")
    seg = CustomerSegmentation(n_clusters=3)
    print("    ✅ CustomerSegmentation initialized")
    print(f"    ✅ Attributes: random_state={seg.random_state}, n_clusters={seg.n_clusters}")
    
    print("\n[3] Loading customer data...")
    data = pd.read_csv('data/customers.csv')
    print(f"    ✅ Data loaded: {len(data)} customers")
    
    print("\n[4] Running segmentation...")
    result = seg.get_customer_segments(data)
    print(f"    ✅ Segmentation successful: {len(result)} customers processed")
    
    print("\n[5] Verifying output...")
    segments = set(result['segment'].values)
    print(f"    ✅ Segments created: {segments}")
    
    print("\n[6] Checking statistics...")
    stats = seg.get_segment_statistics(data)
    for segment_name, stat in stats.items():
        print(f"    ✅ {segment_name}: {stat['count']} customers")
    
    print("\n" + "=" * 60)
    print("✅ ALL SYSTEM LAUNCH CHECKS PASSED")
    print("=" * 60)
    print("\nSystem Status: OPERATIONAL")
    print("No errors detected during startup")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
