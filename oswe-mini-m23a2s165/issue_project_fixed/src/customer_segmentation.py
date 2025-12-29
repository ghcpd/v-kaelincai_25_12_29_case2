"""
Customer Segmentation Module (fixed - deterministic KMeans)

This is a deterministic/fixed version of the original implementation.
The only functional change is setting a fixed `random_state` for KMeans
initialization so clustering results are reproducible across runs.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, List


class CustomerSegmentation:
    """
    Performs customer segmentation using K-means clustering algorithm.
    Deterministic: KMeans is initialized with a fixed `random_state`.
    """

    def __init__(self, n_clusters: int = 3):
        """
        Initialize the customer segmentation model.

        Args:
            n_clusters: Number of customer segments to create (default: 3)
        """
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        # FIX: set random_state to ensure deterministic initialization
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.segment_labels = None
        self.is_fitted = False

    def load_data(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def fit(self, data: pd.DataFrame) -> 'CustomerSegmentation':
        features = data[['monthly_spending', 'visit_frequency']].values
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled)
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
