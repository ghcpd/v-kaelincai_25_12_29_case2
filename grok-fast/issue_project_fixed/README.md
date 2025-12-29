# Customer Segmentation - Fixed Version

A Python project demonstrating **deterministic behavior** in K-means clustering customer segmentation. This project contains the **fixed version** of the original flaky behavior bug.

## 🎯 Project Purpose

This project demonstrates the **solution** to a real-world Flaky Behavior bug where:
- ✅ **Same input** (identical customer data)
- ✅ **Consistent output** (identical cluster assignments each run)
- 🛠️ **Fix**: Added `random_state=42` parameter to K-means initialization

## 📁 Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── customer_segmentation.py    # Fixed core module
├── tests/
│   ├── __init__.py
│   └── test_segmentation.py        # Tests that now pass consistently
├── data/
│   └── customers.csv               # Sample customer data (50 customers)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── FIX_SUMMARY.md                  # Documentation of the fix
```

## 🛠️ The Fix

**Problem**: K-means algorithm initialized without `random_state` parameter

**Solution**: Added `random_state=42` to ensure deterministic behavior

**Impact**:
- Each run produces identical cluster assignments
- Tests pass consistently (no more flaky tests)
- Business reports show stable customer segments
- "High-value" customers are always classified as "High-value"

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows 11 (tested on this platform)

### Installation & Running Tests

**One-line setup and test**:
```powershell
pip install -r requirements.txt ; pytest tests/test_segmentation.py -v
```

**Or step by step**:
```powershell
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/test_segmentation.py -v

# Run specific test multiple times to verify consistency
pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_same_input_produces_same_clusters_run_twice -v
```

## 🧪 Test Results

### Expected Behavior

When running the test suite, all tests should **pass consistently**:

**Every Run** (should always pass):
```
test_same_input_produces_same_clusters_run_twice PASSED
test_multiple_runs_produce_consistent_results PASSED
test_customer_segment_assignment_stability PASSED
test_segment_count_stability PASSED
test_boundary_customer_stability PASSED
```

### Deterministic Tests Included

1. **`test_same_input_produces_same_clusters_run_twice`**
   - Now passes 100% of the time
   - Verifies that two runs produce identical results

2. **`test_customer_segment_assignment_stability`**
   - Now passes 100% of the time
   - Verifies specific customers stay in their segments

3. **`test_multiple_runs_produce_consistent_results`**
   - Now passes 100% of the time
   - Runs clustering 5 times, expects identical results

4. **`test_segment_count_stability`**
   - Now passes 100% of the time
   - Verifies segment sizes remain consistent

5. **`test_boundary_customer_stability`**
   - Now passes 100% of the time
   - Tests customers near cluster boundaries

## 📊 Sample Data

The [data/customers.csv](data/customers.csv) file contains 50 customers with:
- `customer_id`: Unique identifier (C001-C050)
- `monthly_spending`: Amount spent per month ($140-$950)
- `visit_frequency`: Number of visits per month (2-26)

Customers are distributed across three natural groups:
- **Low-engagement**: ~$150/month, ~3 visits
- **Regular**: ~$500/month, ~11 visits
- **High-value**: ~$920/month, ~25 visits

## 🔍 Verifying the Fix

### Method 1: Run Tests Multiple Times
```powershell
# Run the same test 10 times - all should pass
for ($i=1; $i -le 10; $i++) {
    Write-Host "--- Run $i ---"
    pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_same_input_produces_same_clusters_run_twice -v
}
```

### Method 2: Interactive Python
```python
import sys
sys.path.append('src')
from customer_segmentation import segment_customers

# Run twice with same data
result1, stats1 = segment_customers('data/customers.csv')
result2, stats2 = segment_customers('data/customers.csv')

# Compare cluster assignments
print("Run 1 clusters:", result1['cluster'].values)
print("Run 2 clusters:", result2['cluster'].values)
print("Are they equal?", (result1['cluster'].values == result2['cluster'].values).all())
# Output: True (always)
```

## 📚 Learn More

See [FIX_SUMMARY.md](FIX_SUMMARY.md) for:
- Detailed problem analysis
- Step-by-step fix implementation
- Why the fix works
- Testing verification

## 🏷️ Fix Classification

**Category**: Flaky Behavior Fix
- **Pattern**: Same input → Consistent outputs
- **Solution**: Deterministic algorithm initialization
- **Complexity**: Simple (single-parameter addition)
- **Reliability**: 100% consistent results

## 📝 License

This is a demonstration project for educational purposes.