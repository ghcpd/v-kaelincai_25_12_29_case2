"""
Test suite for customer segmentation module.

These tests demonstrate the FLAKY BEHAVIOR issue where the same input
produces inconsistent outputs due to non-deterministic K-means initialization.

Expected behavior: Tests should FAIL intermittently, demonstrating the bug.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from customer_segmentation import CustomerSegmentation, segment_customers


class TestCustomerSegmentationDeterminism:
    """
    Tests that demonstrate non-deterministic behavior in customer segmentation.
    
    EXPECTED: These tests should fail intermittently (flaky tests)
    """
    
    @pytest.fixture
    def sample_data(self):
        """Create sample customer data for testing."""
        return pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006'],
            'monthly_spending': [500.0, 510.0, 150.0, 920.0, 495.0, 160.0],
            'visit_frequency': [12, 13, 3, 25, 11, 4]
        })
    
    @pytest.fixture
    def data_filepath(self):
        """Get path to the customer data CSV file."""
        test_dir = os.path.dirname(__file__)
        return os.path.join(test_dir, '..', 'data', 'customers.csv')
    
    def test_same_input_produces_same_clusters_run_twice(self, sample_data):
        """
        FLAKY TEST: Running segmentation twice on same data should produce same results.
        
        Issue: Due to random initialization in K-means (missing random_state),
        this test fails intermittently.
        
        Expected: FAILS ~30-50% of the time
        Location: src/customer_segmentation.py, line 41 (KMeans initialization)
        """
        segmenter1 = CustomerSegmentation(n_clusters=3)
        clusters1 = segmenter1.fit_predict(sample_data)
        
        segmenter2 = CustomerSegmentation(n_clusters=3)
        clusters2 = segmenter2.fit_predict(sample_data)
        
        # This assertion should pass if algorithm is deterministic
        # but FAILS intermittently due to random initialization
        np.testing.assert_array_equal(
            clusters1, 
            clusters2,
            err_msg="Same input data produced different cluster assignments!"
        )
    
    def test_customer_segment_assignment_stability(self, sample_data):
        """
        FLAKY TEST: Specific customers should be consistently assigned to same segments.
        
        Issue: Customer C004 (high spender: $920, 25 visits) should always be
        in the "High-value" segment, but due to random initialization,
        sometimes gets assigned to different clusters.
        
        Expected: FAILS intermittently
        Location: src/customer_segmentation.py, line 41
        """
        segmenter = CustomerSegmentation(n_clusters=3)
        segmented_data = segmenter.get_customer_segments(sample_data)
        
        # High spender should be in "High-value" segment
        high_spender = segmented_data[segmented_data['customer_id'] == 'C004']
        assert high_spender['segment'].values[0] == 'High-value', \
            f"Customer C004 (high spender) should be in 'High-value' segment, " \
            f"but got '{high_spender['segment'].values[0]}'"
        
        # Low spender should be in "Low-engagement" segment
        low_spender = segmented_data[segmented_data['customer_id'] == 'C003']
        assert low_spender['segment'].values[0] == 'Low-engagement', \
            f"Customer C003 (low spender) should be in 'Low-engagement' segment, " \
            f"but got '{low_spender['segment'].values[0]}'"
    
    def test_multiple_runs_produce_consistent_results(self, data_filepath):
        """
        FLAKY TEST: Multiple segmentation runs should produce identical results.
        
        Issue: Running the segmentation algorithm 5 times on the same dataset
        should produce identical cluster assignments each time if deterministic.
        
        Expected: FAILS most of the time (>80%)
        Location: src/customer_segmentation.py, line 41
        """
        data = pd.read_csv(data_filepath)
        
        # Run segmentation 5 times
        all_results = []
        for i in range(5):
            segmenter = CustomerSegmentation(n_clusters=3)
            clusters = segmenter.fit_predict(data)
            all_results.append(clusters)
        
        # All results should be identical
        first_result = all_results[0]
        for i, result in enumerate(all_results[1:], start=2):
            np.testing.assert_array_equal(
                first_result,
                result,
                err_msg=f"Run 1 and Run {i} produced different cluster assignments!"
            )
    
    def test_segment_count_stability(self, data_filepath):
        """
        FLAKY TEST: Each segment should have consistent customer count across runs.
        
        Issue: The number of customers in "High-value" segment should be stable,
        but varies due to non-deterministic clustering.
        
        Expected: FAILS intermittently (~40%)
        Location: src/customer_segmentation.py, line 41
        """
        data = pd.read_csv(data_filepath)
        
        # First run
        _, stats1 = segment_customers(data_filepath, n_clusters=3)
        high_value_count1 = stats1.get('High-value', {}).get('count', 0)
        
        # Second run
        _, stats2 = segment_customers(data_filepath, n_clusters=3)
        high_value_count2 = stats2.get('High-value', {}).get('count', 0)
        
        assert high_value_count1 == high_value_count2, \
            f"High-value segment had {high_value_count1} customers in first run, " \
            f"but {high_value_count2} customers in second run. Results are not reproducible!"
    
    def test_boundary_customer_stability(self, data_filepath):
        """
        FLAKY TEST: Customers near cluster boundaries should have stable assignments.
        
        Issue: Customer C016 has spending=$500.10 and visits=11, placing them
        near the boundary between "Regular" and "High-value" segments.
        Their assignment should be stable, but isn't.
        
        Expected: FAILS very frequently (>60%)
        Location: src/customer_segmentation.py, line 41
        """
        # Run segmentation multiple times
        assignments = []
        
        for _ in range(10):
            segmenter = CustomerSegmentation(n_clusters=3)
            data = pd.read_csv(data_filepath)
            segmented = segmenter.get_customer_segments(data)
            
            # Get segment for boundary customer C016
            c016_segment = segmented[segmented['customer_id'] == 'C016']['segment'].values[0]
            assignments.append(c016_segment)
        
        # All assignments should be the same
        unique_assignments = set(assignments)
        assert len(unique_assignments) == 1, \
            f"Customer C016 was assigned to different segments across runs: {unique_assignments}. " \
            f"This indicates non-deterministic behavior!"


class TestCustomerSegmentationBasicFunctionality:
    """
    Basic functionality tests that should pass (not related to the flaky bug).
    """
    
    @pytest.fixture
    def sample_data(self):
        """Create sample customer data for testing."""
        return pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'monthly_spending': [500.0, 150.0, 900.0],
            'visit_frequency': [12, 3, 25]
        })
    
    def test_model_initialization(self):
        """Test that model can be initialized."""
        segmenter = CustomerSegmentation(n_clusters=3)
        assert segmenter.n_clusters == 3
        assert not segmenter.is_fitted
    
    def test_fit_predict_returns_correct_shape(self, sample_data):
        """Test that fit_predict returns array with correct length."""
        segmenter = CustomerSegmentation(n_clusters=3)
        clusters = segmenter.fit_predict(sample_data)
        
        assert len(clusters) == len(sample_data)
        assert all(0 <= c < 3 for c in clusters)
    
    def test_get_customer_segments_adds_columns(self, sample_data):
        """Test that get_customer_segments adds cluster and segment columns."""
        segmenter = CustomerSegmentation(n_clusters=3)
        result = segmenter.get_customer_segments(sample_data)
        
        assert 'cluster' in result.columns
        assert 'segment' in result.columns
        assert len(result) == len(sample_data)
    
    def test_predict_before_fit_raises_error(self, sample_data):
        """Test that calling predict before fit raises ValueError."""
        segmenter = CustomerSegmentation(n_clusters=3)
        
        with pytest.raises(ValueError, match="Model must be fitted"):
            segmenter.predict(sample_data)


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '--tb=short'])
