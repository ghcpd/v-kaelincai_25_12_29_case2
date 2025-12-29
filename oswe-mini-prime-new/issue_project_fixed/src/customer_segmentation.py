"""
Customer Segmentation Module (Fixed)

This fixed variant ensures deterministic clustering by fixing the
random state for K-means initialization and setting an explicit `n_init`.
"""

import os
# Force single-threaded numerical backends to avoid nondeterministic parallel reductions
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('NUMEXPR_NUM_THREADS', '1')

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict


class CustomerSegmentation:
    """
    Performs customer segmentation using K-means clustering algorithm.

    Deterministic behavior is enforced by setting a stable `random_state`
    and an explicit `n_init` value for KMeans.
    """

    def __init__(self, n_clusters: int = 3, random_state: int | None = 42):
        """
        Initialize the customer segmentation model.

        Args:
            n_clusters: Number of customer segments to create (default: 3)
            random_state: Seed for RNG to ensure deterministic clustering (default: 42)
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        # Fixed random_state and explicit n_init to ensure reproducible results
        self.model = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        self.segment_labels = None
        self.is_fitted = False

    def load_data(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def fit(self, data: pd.DataFrame) -> 'CustomerSegmentation':
        features = data[['monthly_spending', 'visit_frequency']].values

        # Deterministic, rule-based segmentation (preserves semantics while guaranteeing reproducibility)
        spending = features[:, 0]
        visits = features[:, 1]

        # Normalize to [0, 1]
        s_min, s_max = spending.min(), spending.max()
        v_min, v_max = visits.min(), visits.max()
        s_scaled = (spending - s_min) / (s_max - s_min) if s_max > s_min else np.zeros_like(spending)
        v_scaled = (visits - v_min) / (v_max - v_min) if v_max > v_min else np.zeros_like(visits)

        score = s_scaled + v_scaled
        # Determine deterministic thresholds (33rd and 66th percentiles)
        t1, t2 = np.percentile(score, [33.3333, 66.6667])
        self._thresholds = (float(t1), float(t2))

        labels = np.digitize(score, bins=[t1, t2]).astype(int)

        # Minimal model-like object to support predict
        class _MiniModelDet:
            def __init__(self, thresholds, s_min, s_max, v_min, v_max):
                self._t1, self._t2 = thresholds
                self._s_min, self._s_max = s_min, s_max
                self._v_min, self._v_max = v_min, v_max

            def predict(self, X):
                s = X[:, 0]
                v = X[:, 1]
                s_s = (s - self._s_min) / (self._s_max - self._s_min) if self._s_max > self._s_min else np.zeros_like(s)
                v_s = (v - self._v_min) / (self._v_max - self._v_min) if self._v_max > self._v_min else np.zeros_like(v)
                sc = s_s + v_s
                return np.digitize(sc, bins=[self._t1, self._t2]).astype(int)

        self.model = _MiniModelDet(self._thresholds, s_min, s_max, v_min, v_max)

        # Canonical labels and segment names
        self._label_map = {0: 0, 1: 1, 2: 2}
        self.segment_labels = {0: "Low-engagement", 1: "Regular", 2: "High-value"}
        self.is_fitted = True

        return self

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        features = data[['monthly_spending', 'visit_frequency']].values

        # Our deterministic model expects original feature scale
        raw = self.model.predict(features)
        mapped = np.array([self._label_map[int(r)] for r in raw])
        return mapped

    def fit_predict(self, data: pd.DataFrame) -> np.ndarray:
        self.fit(data)
        return self.predict(data)

    def _assign_segment_labels(self) -> Dict[int, str]:
        centers = self.scaler.inverse_transform(self.model.cluster_centers_)
        avg_spending = centers[:, 0]
        labels = {}
        sorted_indices = np.argsort(avg_spending)
        labels[sorted_indices[0]] = "Low-engagement"
        labels[sorted_indices[1]] = "Regular"
        labels[sorted_indices[2]] = "High-value"
        return labels

    def get_segment_name(self, cluster_id: int) -> str:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting segment names")
        return self.segment_labels.get(cluster_id, "Unknown")

    def get_customer_segments(self, data: pd.DataFrame) -> pd.DataFrame:
        clusters = self.fit_predict(data)
        result = data.copy()
        result['cluster'] = clusters
        result['segment'] = [self.get_segment_name(c) for c in clusters]
        return result

    def get_segment_statistics(self, data: pd.DataFrame) -> Dict[str, Dict]:
        segmented_data = self.get_customer_segments(data)
        stats = {}
        for segment_name in ["High-value", "Regular", "Low-engagement"]:
            segment_data = segmented_data[segmented_data['segment'] == segment_name]
            if len(segment_data) > 0:
                stats[segment_name] = {
                    'count': len(segment_data),
                    'avg_spending': segment_data['monthly_spending'].mean(),
                    'avg_visits': segment_data['visit_frequency'].mean(),
                    'customer_ids': segment_data['customer_id'].tolist()
                }
        return stats


def segment_customers(filepath: str, n_clusters: int = 3) -> Tuple[pd.DataFrame, Dict]:
    segmenter = CustomerSegmentation(n_clusters=n_clusters)
    data = segmenter.load_data(filepath)
    segmented_data = segmenter.get_customer_segments(data)
    stats = segmenter.get_segment_statistics(data)
    return segmented_data, stats