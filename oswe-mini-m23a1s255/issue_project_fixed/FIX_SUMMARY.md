FIX SUMMARY — Customer Segmentation (determinism fix)

1) Problem identification

- Root cause: KMeans in `src/customer_segmentation.py` was instantiated
  without a `random_state` (and with an implicit/version-dependent
  `n_init`). This allowed different random initial centroids across
  runs which produced non-deterministic cluster assignments.
- Specific code: CustomerSegmentation.__init__ (original line where
  `KMeans(n_clusters=n_clusters)` was created).
- Why flaky: K-means uses random initialization; without a fixed RNG
  seed different runs can converge to different local minima producing
  inconsistent labels and segment counts.

2) Solution implemented

- Made RNG explicit: `CustomerSegmentation.__init__` accepts an
  optional `random_state` (default=42) and passes it to `KMeans`.
- Fixed `n_init` to an explicit integer (10) to avoid scikit-learn
  version-dependent behavior.
- Added a stable tie-break in `_assign_segment_labels` using a
  lexicographic sort (avg_spending, avg_visits, cluster_id) so that
  cluster->segment mapping is repeatable even when centers are close.
- Preserved the original algorithm and API compatibility; the
  deterministic behavior is opt-out via `random_state=None`.

Trade-offs
- Setting a default seed enforces reproducibility (desirable for
  production & tests). For randomized exploration you can still pass
  `random_state=None` to get non-deterministic behavior.
- No change to the algorithmic logic or clustering objective.

3) Testing & validation

- All existing tests were copied unchanged into `issue_project_fixed/`.
- Validation performed by running the determinism test-suite 10 times
  and confirming identical results across runs.

How you can reproduce locally

1. Install
   pip install -r requirements.txt
2. Run deterministic tests 10×
   for ($i=1; $i -le 10; $i++) { pytest tests/test_segmentation.py::TestCustomerSegmentationDeterminism -q }
3. Expected: 10/10 runs PASS and produce identical cluster assignments.

4) Additional improvements / notes

- Explicit `n_init` reduces risk of behavior changes across
  scikit-learn versions.
- Stable tie-breaking improves robustness for boundary cases.
- The code remains backward-compatible: passing `random_state=None`
  restores the original non-deterministic behavior if desired.

Files changed/added in fixed copy
- src/customer_segmentation.py  (deterministic implementation)
- tests/test_segmentation.py   (copied, unchanged)
- FIX_SUMMARY.md              (this file)
- README.md                   (updated instructions)

Status: Fixed — deterministic across repeated runs (meets all
validation requirements from the task brief).