# Tests copied from original project (kept unchanged)

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from customer_segmentation import CustomerSegmentation, segment_customers


class TestCustomerSegmentationDeterminism:

    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006'],
            'monthly_spending': [500.0, 510.0, 150.0, 920.0, 495.0, 160.0],
            'visit_frequency': [12, 13, 3, 25, 11, 4]
        })

    @pytest.fixture
    def data_filepath(self):
        test_dir = os.path.dirname(__file__)
        return os.path.join(test_dir, '..', 'data', 'customers.csv')

    def test_same_input_produces_same_clusters_run_twice(self, sample_data):
        segmenter1 = CustomerSegmentation(n_clusters=3)
        clusters1 = segmenter1.fit_predict(sample_data)
        segmenter2 = CustomerSegmentation(n_clusters=3)
        clusters2 = segmenter2.fit_predict(sample_data)
        np.testing.assert_array_equal(clusters1, clusters2)

    def test_customer_segment_assignment_stability(self, sample_data):
        segmenter = CustomerSegmentation(n_clusters=3)
        segmented_data = segmenter.get_customer_segments(sample_data)
        high_spender = segmented_data[segmented_data['customer_id'] == 'C004']
        assert high_spender['segment'].values[0] == 'High-value'
        low_spender = segmented_data[segmented_data['customer_id'] == 'C003']
        assert low_spender['segment'].values[0] == 'Low-engagement'

    def test_multiple_runs_produce_consistent_results(self, data_filepath):
        data = pd.read_csv(data_filepath)
        all_results = []
        for i in range(5):
            segmenter = CustomerSegmentation(n_clusters=3)
            clusters = segmenter.fit_predict(data)
            all_results.append(clusters)
        first_result = all_results[0]
        for result in all_results[1:]:
            np.testing.assert_array_equal(first_result, result)

    def test_segment_count_stability(self, data_filepath):
        data = pd.read_csv(data_filepath)
        _, stats1 = segment_customers(data_filepath, n_clusters=3)
        high_value_count1 = stats1.get('High-value', {}).get('count', 0)
        _, stats2 = segment_customers(data_filepath, n_clusters=3)
        high_value_count2 = stats2.get('High-value', {}).get('count', 0)
        assert high_value_count1 == high_value_count2

    def test_boundary_customer_stability(self, data_filepath):
        assignments = []
        for _ in range(10):
            segmenter = CustomerSegmentation(n_clusters=3)
            data = pd.read_csv(data_filepath)
            segmented = segmenter.get_customer_segments(data)
            c016_segment = segmented[segmented['customer_id'] == 'C016']['segment'].values[0]
            assignments.append(c016_segment)
        unique_assignments = set(assignments)
        assert len(unique_assignments) == 1


class TestCustomerSegmentationBasicFunctionality:

    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'monthly_spending': [500.0, 150.0, 900.0],
            'visit_frequency': [12, 3, 25]
        })

    def test_model_initialization(self):
        segmenter = CustomerSegmentation(n_clusters=3)
        assert segmenter.n_clusters == 3
        assert not segmenter.is_fitted

    def test_fit_predict_returns_correct_shape(self, sample_data):
        segmenter = CustomerSegmentation(n_clusters=3)
        clusters = segmenter.fit_predict(sample_data)
        assert len(clusters) == len(sample_data)
        assert all(0 <= c < 3 for c in clusters)

    def test_get_customer_segments_adds_columns(self, sample_data):
        segmenter = CustomerSegmentation(n_clusters=3)
        result = segmenter.get_customer_segments(sample_data)
        assert 'cluster' in result.columns
        assert 'segment' in result.columns
        assert len(result) == len(sample_data)

    def test_predict_before_fit_raises_error(self, sample_data):
        segmenter = CustomerSegmentation(n_clusters=3)
        with pytest.raises(ValueError, match="Model must be fitted"):
            segmenter.predict(sample_data)
