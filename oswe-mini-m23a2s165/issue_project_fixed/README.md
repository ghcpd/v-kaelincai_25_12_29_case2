# Customer Segmentation — Fixed (deterministic)

This repository is a fixed copy of the original `issue_project/` where the
K-means initialization was non-deterministic. The only functional change is
setting a fixed `random_state` for `KMeans` so results are reproducible.

Quick verification:

```powershell
cd issue_project_fixed
pip install -r requirements.txt
# Run the determinism tests 10 times — all runs should pass and produce identical results
for ($i=1; $i -le 10; $i++) { pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism -q }
```

Files changed from original:
- `src/customer_segmentation.py` — fixed KMeans initialization (deterministic)
- `FIX_SUMMARY.md` — details of the fix and verification steps

All other code, tests and data are unchanged from the original project.
