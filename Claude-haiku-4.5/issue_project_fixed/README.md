# Customer Segmentation - Fixed Version ✅

A Python project demonstrating **deterministic customer segmentation** using K-means clustering. This is the **FIXED version** of the customer segmentation module where all flaky behavior has been resolved.

## 🎯 Project Purpose

This project demonstrates the **solution** to a Flaky Behavior bug pattern where:
- ✅ **Same input** (identical customer data)
- ✅ **Consistent output** (identical cluster assignments every run)
- ✅ **Root cause fixed**: Added `random_state` parameter to K-means initialization

## 📁 Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── customer_segmentation.py    # Fixed implementation
├── tests/
│   ├── __init__.py
│   └── test_segmentation.py        # All tests now pass consistently
├── data/
│   └── customers.csv               # Sample customer data (50 customers)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── FIX_SUMMARY.md                  # Detailed fix documentation
```

## ✅ The Fix

**Problem Fixed**: K-means algorithm now initialized with `random_state` parameter

**Changes Made**:
```python
# Before (Line 41):
self.model = KMeans(n_clusters=n_clusters)

# After:
self.model = KMeans(n_clusters=n_clusters, random_state=42)
```

**Impact**:
- ✅ All tests pass 100% of the time
- ✅ Same input produces identical cluster assignments
- ✅ Segment counts remain stable across runs
- ✅ Boundary customers consistently assigned to same segments
- ✅ Zero test flakiness in CI/CD pipeline

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Windows, macOS, or Linux

### Installation & Running Tests

**Install dependencies**:
```powershell
pip install -r requirements.txt
```

**Run all tests**:
```powershell
pytest tests/test_segmentation.py -v
```

**Expected output** (all tests pass):
```
tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_same_input_produces_same_clusters_run_twice PASSED
tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_customer_segment_assignment_stability PASSED
tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_multiple_runs_produce_consistent_results PASSED
tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_segment_count_stability PASSED
tests/test_segmentation.py::TestCustomerSegmentationDeterminism::test_boundary_customer_stability PASSED
tests/test_segmentation.py::TestCustomerSegmentationBasicFunctionality::test_model_initialization PASSED
tests/test_segmentation.py::TestCustomerSegmentationBasicFunctionality::test_fit_predict_returns_correct_shape PASSED
tests/test_segmentation.py::TestCustomerSegmentationBasicFunctionality::test_get_customer_segments_adds_columns PASSED
tests/test_segmentation.py::TestCustomerSegmentationBasicFunctionality::test_predict_before_fit_raises_error PASSED

======================== 9 passed in 0.15s ========================
```

## 📚 Usage Example

```python
import pandas as pd
from src.customer_segmentation import CustomerSegmentation, segment_customers

# Load data
data = pd.read_csv('data/customers.csv')

# Method 1: Using the main class
segmenter = CustomerSegmentation(n_clusters=3, random_state=42)
segmented_data = segmenter.get_customer_segments(data)
stats = segmenter.get_segment_statistics(data)

# Method 2: Using convenience function
segmented_data, stats = segment_customers('data/customers.csv')

# View results
print(segmented_data[['customer_id', 'segment']])
print(stats)
```

## 🔍 Verify Deterministic Behavior

Run tests 10 times - all should pass with identical results:

```powershell
for ($i=1; $i -le 10; $i++) {
    Write-Host "=== Test Run $i ==="
    pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism -v
}
```

**Expected**: All 10 runs pass with 100% consistency.

## 📖 Documentation

See [FIX_SUMMARY.md](FIX_SUMMARY.md) for:
- Detailed root cause analysis
- Solution explanation
- Testing verification procedure
- Code quality improvements
- Best practices and lessons learned

## 🏆 What's Changed from Original

1. **Added `random_state` parameter** to `KMeans` initialization (line 41)
2. **Added `random_state` parameter** to `__init__` method signature (line 25)
3. **Updated `segment_customers` function** to accept and pass `random_state` (line 192)
4. **Updated docstrings** to reflect deterministic behavior
5. **Updated module docstring** to indicate fix is applied
6. **Test comments** updated to reflect fixed behavior

## ✨ Features

- **Deterministic K-means clustering** - Same results every time
- **Reproducible segmentation** - Perfect for production use
- **Three segment categories** - High-value, Regular, Low-engagement
- **Comprehensive statistics** - Per-segment metrics and customer lists
- **Fully tested** - 9 tests covering determinism and functionality
- **Type hints** - Full Python type annotations for IDE support

## 🐛 Original Bug Reference

This is the fixed version. The original broken version is in `issue_project/` for comparison.

Original issue:
- Missing `random_state=42` in `KMeans(n_clusters=n_clusters)` initialization
- Caused non-deterministic behavior where same input produced different outputs
- Tests failed intermittently (30-80% failure rate)
- See `../issue_project/KNOWN_ISSUE.md` for complete documentation

## ✅ Verification Checklist

- [x] All tests pass 100% of the time
- [x] Determinism tests pass consistently (10/10 runs)
- [x] Same input produces identical cluster assignments
- [x] Segment counts remain stable across runs
- [x] Boundary customers stay in same segments
- [x] No changes to algorithm's mathematical correctness
- [x] All existing functionality remains intact
- [x] FIX_SUMMARY.md documents all changes

## 🎓 Learning Outcome

This fixed version demonstrates:
- How to identify non-deterministic behavior in ML systems
- How to use `random_state` parameters for reproducibility
- Importance of testing for determinism
- Best practices for production ML code
- How to document fixes comprehensively

## 📝 File Manifest

- `src/customer_segmentation.py` - Fixed implementation (210 lines)
- `tests/test_segmentation.py` - Test suite (230 lines)
- `data/customers.csv` - Sample data (50 customers)
- `requirements.txt` - Dependencies (4 packages)
- `README.md` - This file
- `FIX_SUMMARY.md` - Detailed fix documentation

## 🔗 Related

- **Original broken version**: `../issue_project/`
- **Fix documentation**: `FIX_SUMMARY.md`
- **Test file**: `tests/test_segmentation.py`
- **Implementation**: `src/customer_segmentation.py`

---

**Status**: ✅ Fixed and verified  
**Determinism**: ✅ 100% deterministic  
**Test pass rate**: ✅ 100%  
**Production ready**: ✅ Yes
