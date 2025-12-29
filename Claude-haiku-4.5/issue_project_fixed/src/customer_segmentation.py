"""
Customer Segmentation Module

This module provides functionality to segment customers into different groups
based on their spending behavior and visit frequency using K-means clustering.

FIX APPLIED: The clustering results are now deterministic with random_state parameter.
See FIX_SUMMARY.md for details.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, List


class CustomerSegmentation:
    """
    Performs customer segmentation using K-means clustering algorithm.
    
    Segments customers into three categories:
    - High-value customers (frequent visits, high spending)
    - Regular customers (moderate visits and spending)
    - Low-engagement customers (infrequent visits, low spending)
    """
    
    def __init__(self, n_clusters: int = 3, random_state: int = 42):
        """
        Initialize the customer segmentation model.
        
        Args:
            n_clusters: Number of customer segments to create (default: 3)
            random_state: Random seed for reproducibility (default: 42)
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        # FIX: Added random_state parameter for deterministic behavior
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state)
        self.segment_labels = None
        self.is_fitted = False
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load customer data from CSV file.
        
        Args:
            filepath: Path to the customer data CSV file
            
        Returns:
            DataFrame containing customer data
        """
        return pd.read_csv(filepath)
    
    def fit(self, data: pd.DataFrame) -> 'CustomerSegmentation':
        """
        Fit the segmentation model on customer data.
        
        Args:
            data: DataFrame with columns 'monthly_spending' and 'visit_frequency'
            
        Returns:
            self for method chaining
        """
        features = data[['monthly_spending', 'visit_frequency']].values
        
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Fit K-means model
        self.model.fit(features_scaled)
        
        # Assign meaningful labels based on cluster centers
        self.segment_labels = self._assign_segment_labels()
        self.is_fitted = True
        
        return self
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict customer segments for given data.
        
        Args:
            data: DataFrame with columns 'monthly_spending' and 'visit_frequency'
            
        Returns:
            Array of cluster labels (0, 1, 2)
            
        Raises:
            ValueError: If model is not fitted yet
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        features = data[['monthly_spending', 'visit_frequency']].values
        features_scaled = self.scaler.transform(features)
        
        return self.model.predict(features_scaled)
    
    def fit_predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Fit the model and predict segments in one step.
        
        Args:
            data: DataFrame with columns 'monthly_spending' and 'visit_frequency'
            
        Returns:
            Array of cluster labels
        """
        self.fit(data)
        return self.predict(data)
    
    def _assign_segment_labels(self) -> Dict[int, str]:
        """
        Assign meaningful labels to clusters based on their centers.
        
        Returns:
            Dictionary mapping cluster ID to segment name
        """
        centers = self.scaler.inverse_transform(self.model.cluster_centers_)
        
        # Calculate average spending for each cluster
        avg_spending = centers[:, 0]
        
        # Map clusters to segment names
        labels = {}
        sorted_indices = np.argsort(avg_spending)
        
        labels[sorted_indices[0]] = "Low-engagement"
        labels[sorted_indices[1]] = "Regular"
        labels[sorted_indices[2]] = "High-value"
        
        return labels
    
    def get_segment_name(self, cluster_id: int) -> str:
        """
        Get the segment name for a given cluster ID.
        
        Args:
            cluster_id: The cluster ID (0, 1, or 2)
            
        Returns:
            Segment name (e.g., "High-value", "Regular", "Low-engagement")
            
        Raises:
            ValueError: If model is not fitted yet
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting segment names")
        
        return self.segment_labels.get(cluster_id, "Unknown")
    
    def get_customer_segments(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Get customer data with assigned segment labels.
        
        Args:
            data: DataFrame with customer data
            
        Returns:
            DataFrame with added 'cluster' and 'segment' columns
        """
        clusters = self.fit_predict(data)
        
        result = data.copy()
        result['cluster'] = clusters
        result['segment'] = [self.get_segment_name(c) for c in clusters]
        
        return result
    
    def get_segment_statistics(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """
        Calculate statistics for each customer segment.
        
        Args:
            data: DataFrame with customer data
            
        Returns:
            Dictionary with statistics for each segment
        """
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


def segment_customers(filepath: str, n_clusters: int = 3, random_state: int = 42) -> Tuple[pd.DataFrame, Dict]:
    """
    Convenience function to segment customers from a CSV file.
    
    Args:
        filepath: Path to customer data CSV file
        n_clusters: Number of segments to create (default: 3)
        random_state: Random seed for reproducibility (default: 42)
        
    Returns:
        Tuple of (segmented_data_dataframe, segment_statistics_dict)
    """
    segmenter = CustomerSegmentation(n_clusters=n_clusters, random_state=random_state)
    data = segmenter.load_data(filepath)
    
    segmented_data = segmenter.get_customer_segments(data)
    stats = segmenter.get_segment_statistics(data)
    
    return segmented_data, stats
