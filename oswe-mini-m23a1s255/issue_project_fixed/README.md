# Customer Segmentation — Fixed (deterministic)

This repository is a fixed copy of the original `issue_project/` that
addresses the non-deterministic (flaky) behavior in the K-means based
customer segmentation implementation.

Key fix: KMeans initialization is now deterministic by default
(random_state is explicit and `n_init` is fixed). Tests that were
previously flaky now pass consistently.

Quick verification

# Windows PowerShell
cd issue_project_fixed
pip install -r requirements.txt
# Run the determinism test 10 times (should pass every time)
for ($i=1; $i -le 10; $i++) {
    Write-Host "=== Test Run $i ==="
    pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism -q
}

API compatibility
- Public API (class name, function names, method signatures) is preserved.
- A new optional `random_state` parameter was added to allow reproducible
  or intentionally non-reproducible runs.

See `FIX_SUMMARY.md` for details about the root cause, the fix, and how
it was validated.