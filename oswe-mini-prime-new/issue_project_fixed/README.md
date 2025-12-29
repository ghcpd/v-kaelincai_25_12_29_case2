# issue_project_fixed

This is the fixed version of the customer segmentation project. The intermittent/flaky clustering behavior has been resolved by enforcing deterministic K-means initialization (fixed `random_state` and explicit `n_init`).

How to run tests:

```powershell
cd issue_project_fixed
pip install -r requirements.txt
pytest -q
```

The tests that previously failed intermittently should now pass consistently across repeated runs.