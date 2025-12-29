"""
Deterministic Customer Segmentation Module (fixed)

This module provides customer segmentation using K-means clustering but
ensures deterministic behavior by making all sources of randomness explicit
and adding stable tie-breaks when labeling clusters.

The fix preserves the original algorithm (K-means) and API while making
results reproducible across runs.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict


class CustomerSegmentation:
    """
    Performs customer segmentation using K-means clustering algorithm.

    This fixed implementation is deterministic by default: the KMeans
    initializer's randomness is controlled via the `random_state` parameter
    and `n_init` is set explicitly to avoid version-dependent defaults.
    """

    def __init__(self, n_clusters: int = 3, random_state: int | None = 42):
        """
        Initialize the customer segmentation model.

        Args:
            n_clusters: Number of customer segments to create (default: 3)
            random_state: Seed for the KMeans RNG. Use `None` for non-deterministic
                          behavior (keeps backward-compatibility).
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        # Make randomness explicit and stable across scikit-learn versions
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.segment_labels = None
        self.is_fitted = False

    def load_data(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def fit(self, data: pd.DataFrame) -> 'CustomerSegmentation':
        features = data[['monthly_spending', 'visit_frequency']].values
        features_scaled = self.scaler.fit_transform(features)

        # Fit K-means model (deterministic when random_state is set)
        self.model.fit(features_scaled)

        # Assign meaningful labels based on cluster centers (stable ordering)
        self.segment_labels = self._assign_segment_labels()
        self.is_fitted = True

        return self

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        features = data[['monthly_spending', 'visit_frequency']].values
        features_scaled = self.scaler.transform(features)

        return self.model.predict(features_scaled)

    def fit_predict(self, data: pd.DataFrame) -> np.ndarray:
        self.fit(data)
        return self.predict(data)

    def _assign_segment_labels(self) -> Dict[int, str]:
        """
        Assign meaningful labels to clusters based on their centers.

        To ensure determinism even when cluster centers are very close (ties),
        we apply a stable lexicographic sort using (avg_spending, avg_visits,
        cluster_id) as the sort key. This guarantees a repeatable mapping from
        cluster id -> semantic label.
        """
        centers = self.scaler.inverse_transform(self.model.cluster_centers_)

        # Primary key: average spending, secondary: average visits, tertiary: cluster id
        avg_spending = centers[:, 0]
        avg_visits = centers[:, 1]
        cluster_ids = np.arange(len(avg_spending))

        # np.lexsort uses the last key as primary, so provide keys in reverse order
        sort_indices = np.lexsort((cluster_ids, avg_visits, avg_spending))

        labels = {}
        labels[sort_indices[0]] = "Low-engagement"
        labels[sort_indices[1]] = "Regular"
        labels[sort_indices[2]] = "High-value"

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


def segment_customers(filepath: str, n_clusters: int = 3, random_state: int | None = 42) -> Tuple[pd.DataFrame, Dict]:
    """Convenience wrapper that preserves determinism by default."""
    segmenter = CustomerSegmentation(n_clusters=n_clusters, random_state=random_state)
    data = segmenter.load_data(filepath)

    segmented_data = segmenter.get_customer_segments(data)
    stats = segmenter.get_segment_statistics(data)

    return segmented_data, stats
