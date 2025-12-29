# Customer Segmentation - Flaky Behavior Demo

A minimal Python project demonstrating **non-deterministic behavior** in K-means clustering customer segmentation. This project intentionally contains a simple bug that causes flaky test failures.

## 🎯 Project Purpose

This project demonstrates a real-world **Flaky Behavior** bug pattern where:
- ✅ **Same input** (identical customer data)
- ❌ **Inconsistent output** (different cluster assignments each run)
- 🐛 **Root cause**: Missing `random_state` parameter in K-means initialization

## 📁 Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── customer_segmentation.py    # Core module with intentional bug
├── tests/
│   ├── __init__.py
│   └── test_segmentation.py        # Flaky tests that fail intermittently
├── data/
│   └── customers.csv               # Sample customer data (50 customers)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── KNOWN_ISSUE.md                  # Bug documentation
```

## 🐛 The Bug

**Problem**: K-means algorithm initialized without `random_state` parameter

**Impact**:
- Each run produces different cluster assignments
- Tests fail intermittently (flaky tests)
- Business reports show inconsistent customer segments
- "High-value" customers might be classified as "Regular" on next run

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

# Run specific flaky test multiple times to see inconsistency
pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_same_input_produces_same_clusters_run_twice -v
```

## 🧪 Test Results

### Expected Behavior

When running the test suite, you should see **flaky failures**:

**Run 1** (might pass):
```
test_same_input_produces_same_clusters_run_twice PASSED
test_multiple_runs_produce_consistent_results PASSED
```

**Run 2** (same tests might fail):
```
test_same_input_produces_same_clusters_run_twice FAILED
test_multiple_runs_produce_consistent_results FAILED
AssertionError: Same input data produced different cluster assignments!
```

### Flaky Tests Included

1. **`test_same_input_produces_same_clusters_run_twice`**
   - Failure rate: ~30-50%
   - Verifies that two runs produce identical results

2. **`test_customer_segment_assignment_stability`**
   - Failure rate: ~20-40%
   - Verifies specific customers stay in their segments

3. **`test_multiple_runs_produce_consistent_results`**
   - Failure rate: ~80%+
   - Runs clustering 5 times, expects identical results

4. **`test_segment_count_stability`**
   - Failure rate: ~40%
   - Verifies segment sizes remain consistent

5. **`test_boundary_customer_stability`**
   - Failure rate: ~60%+
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

## 🔍 Reproducing the Bug

### Method 1: Run Tests Multiple Times
```powershell
# Run the same test 5 times - you'll see different results
for ($i=1; $i -le 5; $i++) {
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
# Output: False (most of the time)
```

## 📚 Learn More

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for:
- Detailed problem analysis
- Why this happens
- Step-by-step fix instructions
- Testing strategies for deterministic behavior

## 🏷️ Bug Classification

**Category**: Flaky Behavior (Bug-related)
- **Pattern**: Same input → Inconsistent outputs
- **Cause**: Non-deterministic algorithm initialization
- **Complexity**: Simple (single-parameter fix)
- **Reproducibility**: High (fails 30-80% of runs depending on test)

## 📝 License

This is a demonstration project for educational purposes.
