# FIX SUMMARY

## Problem Identification
- Root cause: Non-deterministic K-means initialization in `src/customer_segmentation.py`. `KMeans` was instantiated without a fixed `random_state`, causing different cluster assignments across runs.
- Specific code: In `CustomerSegmentation.__init__`, `self.model = KMeans(n_clusters=n_clusters)` (missing `random_state` and explicit `n_init`).
- Why flaky: K-means uses random initialization for centroids when `random_state` is not fixed; different initializations lead to different local minima and thus differing cluster assignments across runs.

## Solution Implemented
- Changes made:
  - Set `random_state` to a fixed value (default: 42) in `KMeans` initialization.
  - Set explicit `n_init=10` to remove future warnings and ensure consistent initialization semantics.
  - Added `random_state` optional parameter to `CustomerSegmentation.__init__` (backward compatible default).
- Why it resolves the issue: Fixing `random_state` ensures K-means uses the same random seed every run, making clustering deterministic given the same input data and environment.
- Trade-offs: Choosing a fixed seed is standard practice for reproducibility; if true randomness is required, the caller can instantiate the class with a different `random_state` or `None`.

## Testing Verification
- How to verify:
  1. Install dependencies: `pip install -r requirements.txt`
  2. Run tests repeatedly:

```powershell
cd issue_project_fixed
for ($i=1; $i -le 10; $i++) {
    Write-Host "=== Test Run $i ==="
    pytest tests/test_segmentation.py -q
}
```

- Expected: All runs pass consistently and test outputs (cluster assignments and counts) remain identical across runs.

## Code Quality / Improvements
- Minimal and targeted change focused on reproducibility; no change to core algorithmic logic (still using K-means).
- Added explicit `n_init` and a documented default `random_state` to make behavior explicit and maintainable.

## Notes
- Original project left unchanged per constraints. The fixed implementation lives under `issue_project_fixed/` and is compatible with existing test expectations and API.
