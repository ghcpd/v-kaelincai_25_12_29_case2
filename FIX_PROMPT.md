# Bug Fix Task - Customer Segmentation Project

## 🎯 Task Objective

You are a senior software engineer tasked with **fixing a flaky behavior bug** in a customer segmentation system. Your goal is to identify and resolve the non-deterministic behavior that causes inconsistent test results.

## 📋 Background

This project contains a customer segmentation module that uses K-means clustering to categorize customers into different groups (High-value, Regular, Low-engagement). However, the system exhibits **flaky behavior** where:

- Same input data produces different outputs on different runs
- Tests pass and fail intermittently without code changes
- Business reports show inconsistent customer segment assignments
- The issue is reproducible but results vary randomly

## 📂 Current Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── customer_segmentation.py
├── tests/
│   ├── __init__.py
│   └── test_segmentation.py
├── data/
│   └── customers.csv
├── requirements.txt
├── README.md
├── KNOWN_ISSUE.md
└── FIX_PROMPT.md (this file)
```

## 🔍 Your Mission

### Step 1: Analyze the Problem

1. Review the failing tests in `tests/test_segmentation.py`
2. Examine the core implementation in `src/customer_segmentation.py`
3. Identify the root cause of non-deterministic behavior
4. Understand why the same input produces different outputs

### Step 2: Create Fixed Version

**IMPORTANT**: Create a **NEW directory** for the fixed version. Do NOT modify the original project.

**Required directory structure**:
```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── customer_segmentation.py    # Fixed implementation
├── tests/
│   ├── __init__.py
│   └── test_segmentation.py        # Same tests, should now pass consistently
├── data/
│   └── customers.csv               # Copy of original data
├── requirements.txt                # Same dependencies
├── README.md                       # Updated to reflect fixes
└── FIX_SUMMARY.md                  # Document your changes
```

### Step 3: Validation Requirements

Your fixed version must:

- ✅ All tests in `TestCustomerSegmentationDeterminism` pass **100% of the time**
- ✅ Running the same test 10 times produces identical results every time
- ✅ Same input data always produces same cluster assignments
- ✅ Segment counts remain stable across multiple runs
- ✅ No changes to the algorithm's mathematical correctness
- ✅ All existing functionality remains intact

### Step 4: Documentation

Create a `FIX_SUMMARY.md` file in the fixed project that includes:

1. **Problem Identification**
   - What was the root cause?
   - Which specific code caused the issue?
   - Why did it cause flaky behavior?

2. **Solution Implemented**
   - What changes were made?
   - Why does this fix resolve the issue?
   - Are there any trade-offs?

3. **Testing Verification**
   - How to verify the fix works?
   - What commands to run?
   - Expected test results

4. **Code Quality**
   - Are there additional improvements made?
   - Any refactoring for better maintainability?

## 🚫 Constraints

- **DO NOT** modify files in `issue_project/` - keep original broken version intact
- **DO** create all fixed files in `issue_project_fixed/`
- **DO NOT** change the algorithm's core logic (still use K-means)
- **DO NOT** modify test assertions (tests should pass as-written)
- **DO** ensure backward compatibility with existing API
- **DO** maintain the same project structure

## 📊 Success Criteria

Your solution is successful when:

```powershell
# Navigate to fixed directory
cd issue_project_fixed

# Install dependencies
pip install -r requirements.txt

# Run tests 10 times - all should pass
for ($i=1; $i -le 10; $i++) {
    Write-Host "=== Test Run $i ==="
    pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism -v
}

# Expected: 10/10 runs pass with identical results
```

## 🎓 Learning Objectives

Through this task, you should demonstrate understanding of:

- Root cause analysis of flaky tests
- Deterministic vs non-deterministic algorithms
- Reproducibility in machine learning systems
- Test-driven debugging methodology
- Code documentation best practices

## 💡 Hints (Read ONLY if stuck)

<details>
<summary>Hint 1: Where to look</summary>

Focus on the initialization of machine learning models. Check if any components rely on randomness.

</details>

<details>
<summary>Hint 2: Common pattern</summary>

Many ML libraries have parameters that control random number generation. Look for such parameters in the scikit-learn documentation.

</details>

<details>
<summary>Hint 3: Solution pattern</summary>

The fix typically involves setting a seed or state parameter to ensure reproducibility. This is a common requirement for production ML systems.

</details>

## 📝 Deliverables Checklist

- [ ] New directory `issue_project_fixed/` created
- [ ] All source files copied and fixed
- [ ] All tests pass consistently (10/10 runs)
- [ ] `FIX_SUMMARY.md` documenting changes
- [ ] Updated `README.md` reflecting the fixed state
- [ ] No modifications to original `issue_project` directory

## 🚀 Get Started

Begin by running the original broken tests to observe the flaky behavior:

```powershell
cd issue_project
pip install -r requirements.txt
pytest tests/test_segmentation.py -v
```

Then analyze the code, identify the issue, and create your fixed version in the new directory.

Good luck! 🎯
