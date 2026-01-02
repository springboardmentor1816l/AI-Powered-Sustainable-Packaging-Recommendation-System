"""
Unit Tests for Material Ranking System
=======================================

Test suite for validating the material ranking logic.

Run with:
    pytest tests/test_ranker.py -v

Author: EcoPackAI Team
Date: 2026-01-02
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import pandas as pd
import numpy as np
from src.recommendation.ranker import MaterialRanker


@pytest.fixture
def sample_data():
    """Create sample material data for testing"""
    np.random.seed(42)
    n_materials = 100
    
    data = {
        'recyclability_percent': np.random.uniform(20, 100, n_materials),
        'recycled_content_percent': np.random.uniform(0, 100, n_materials),
        'material_suitability_score': np.random.uniform(10, 95, n_materials),
        'cost_per_unit_usd': np.random.uniform(1, 50, n_materials),
        'co2_emission_per_kg_estimated': np.random.uniform(0.5, 10, n_materials),
        'load_handling_score': np.random.uniform(1, 10, n_materials),
        'moisture_resistance_score': np.random.uniform(1, 10, n_materials),
        'thermal_resistance_score': np.random.uniform(2, 10, n_materials),
        'supplier_sustainability_compliance_percent': np.random.uniform(60, 100, n_materials),
        'packaging_type': np.random.choice(['Cardboard Boxes', 'Plastic Containers', 'Glass Bottles'], n_materials),
        'supplier_region': np.random.choice(['EMEA', 'AMERICAS', 'APAC'], n_materials)
    }
    
    return pd.DataFrame(data)


@pytest.fixture
def ranker():
    """Create a MaterialRanker instance with default config"""
    return MaterialRanker(ranking_mode='balanced')


class TestMaterialRankerInitialization:
    """Test ranker initialization"""
    
    def test_default_initialization(self):
        """Test ranker initializes with defaults"""
        ranker = MaterialRanker()
        assert ranker.ranking_mode == 'balanced'
        assert len(ranker.weights) > 0
        assert len(ranker.constraints) > 0
    
    def test_mode_selection(self):
        """Test different ranking modes"""
        for mode in ['sustainability_first', 'cost_first', 'balanced']:
            ranker = MaterialRanker(ranking_mode=mode)
            assert ranker.ranking_mode == mode
    
    def test_weights_sum_to_one(self, ranker):
        """Test that weights sum to 1.0"""
        total_weight = sum(ranker.weights.values())
        assert np.isclose(total_weight, 1.0, atol=0.01)


class TestConstraintFiltering:
    """Test constraint filtering logic"""
    
    def test_apply_constraints(self, ranker, sample_data):
        """Test that constraints filter materials"""
        initial_count = len(sample_data)
        df_filtered = ranker.apply_constraints(sample_data)
        
        # Should have some materials (not all filtered)
        assert len(df_filtered) > 0
        assert len(df_filtered) <= initial_count
    
    def test_recyclability_constraint(self, ranker, sample_data):
        """Test recyclability constraint"""
        ranker.constraints['min_recyclability_percent'] = 80.0
        df_filtered = ranker.apply_constraints(sample_data)
        
        # All remaining materials should meet constraint
        assert df_filtered['recyclability_percent'].min() >= 80.0
    
    def test_cost_constraint(self, ranker, sample_data):
        """Test cost constraint"""
        ranker.constraints['max_cost_per_unit'] = 25.0
        df_filtered = ranker.apply_constraints(sample_data)
        
        # All remaining materials should meet constraint
        assert df_filtered['cost_per_unit_usd'].max() <= 25.0
    
    def test_strict_constraints_filter_all(self, ranker, sample_data):
        """Test that very strict constraints can filter all materials"""
        ranker.constraints['min_recyclability_percent'] = 150.0  # Impossible
        df_filtered = ranker.apply_constraints(sample_data)
        
        # Should filter all materials
        assert len(df_filtered) == 0


class TestNormalization:
    """Test feature normalization"""
    
    def test_min_max_normalization(self, ranker, sample_data):
        """Test min-max normalization produces [0, 1] range"""
        ranker.normalization_config['method'] = 'min_max'
        features = ['cost_per_unit_usd', 'co2_emission_per_kg_estimated']
        
        df_norm = ranker.normalize_features(sample_data, features)
        
        for feature in features:
            norm_col = f'{feature}_norm'
            assert norm_col in df_norm.columns
            assert df_norm[norm_col].min() >= 0.0
            assert df_norm[norm_col].max() <= 1.0
    
    def test_z_score_normalization(self, ranker, sample_data):
        """Test z-score normalization"""
        ranker.normalization_config['method'] = 'z_score'
        features = ['cost_per_unit_usd']
        
        df_norm = ranker.normalize_features(sample_data, features)
        
        norm_col = f'{features[0]}_norm'
        assert norm_col in df_norm.columns
        assert df_norm[norm_col].min() >= 0.0
        assert df_norm[norm_col].max() <= 1.0
    
    def test_robust_normalization(self, ranker, sample_data):
        """Test robust normalization"""
        ranker.normalization_config['method'] = 'robust'
        features = ['recyclability_percent']
        
        df_norm = ranker.normalize_features(sample_data, features)
        
        norm_col = f'{features[0]}_norm'
        assert norm_col in df_norm.columns


class TestRankingScore:
    """Test ranking score calculation"""
    
    def test_calculate_ranking_score(self, ranker, sample_data):
        """Test score calculation"""
        df_scored = ranker.calculate_ranking_score(sample_data)
        
        assert 'ranking_score' in df_scored.columns
        assert df_scored['ranking_score'].min() >= 0.0
        assert df_scored['ranking_score'].max() <= 1.1  # Allow for bonus
    
    def test_score_components(self, ranker, sample_data):
        """Test that score components are created"""
        df_scored = ranker.calculate_ranking_score(sample_data)
        
        # Check for score breakdown columns
        score_cols = [col for col in df_scored.columns if col.startswith('score_')]
        assert len(score_cols) > 0
    
    def test_sustainability_bonus(self, ranker, sample_data):
        """Test sustainability bonus application"""
        # Enable bonus
        ranker.advanced_config['sustainability_bonus'] = {
            'enabled': True,
            'recyclability_threshold': 90.0,
            'bonus_multiplier': 1.1
        }
        
        # Set some materials above threshold
        sample_data.loc[:5, 'recyclability_percent'] = 95.0
        
        df_scored = ranker.calculate_ranking_score(sample_data)
        
        # Check bonus was applied
        if 'sustainability_bonus_applied' in df_scored.columns:
            assert df_scored['sustainability_bonus_applied'].sum() > 0


class TestMaterialRanking:
    """Test material ranking"""
    
    def test_rank_materials(self, ranker, sample_data):
        """Test basic ranking"""
        df_ranked = ranker.rank_materials(sample_data)
        
        assert 'rank' in df_ranked.columns
        assert 'ranking_score' in df_ranked.columns
        assert df_ranked['rank'].min() == 1
        assert len(df_ranked) > 0
    
    def test_ranking_order(self, ranker, sample_data):
        """Test that materials are ranked in descending score order"""
        df_ranked = ranker.rank_materials(sample_data)
        
        # Scores should be in descending order for sequential ranks
        prev_score = float('inf')
        for _, row in df_ranked.iterrows():
            assert row['ranking_score'] <= prev_score
            prev_score = row['ranking_score']
    
    def test_grouped_ranking(self, ranker, sample_data):
        """Test ranking by groups"""
        df_ranked = ranker.rank_materials(sample_data, group_by='packaging_type')
        
        # Each group should have its own rank 1
        for group in sample_data['packaging_type'].unique():
            group_data = df_ranked[df_ranked['packaging_type'] == group]
            if len(group_data) > 0:
                assert group_data['rank'].min() == 1


class TestTopRecommendations:
    """Test top-N recommendations"""
    
    def test_get_top_n(self, ranker, sample_data):
        """Test getting top N materials"""
        df_ranked = ranker.rank_materials(sample_data)
        df_top = ranker.get_top_recommendations(df_ranked, top_n=5)
        
        assert len(df_top) <= 5
        assert all(df_top['rank'] <= 5)
    
    def test_top_n_per_group(self, ranker, sample_data):
        """Test getting top N per group"""
        df_ranked = ranker.rank_materials(sample_data, group_by='packaging_type')
        df_top = ranker.get_top_recommendations(df_ranked, top_n=3, group_by='packaging_type')
        
        # Should have up to 3 materials per group
        for group in df_top['packaging_type'].unique():
            group_count = len(df_top[df_top['packaging_type'] == group])
            assert group_count <= 3


class TestDeterminism:
    """Test that rankings are deterministic"""
    
    def test_deterministic_ranking(self, ranker, sample_data):
        """Test that same input produces same output"""
        df_ranked_1 = ranker.rank_materials(sample_data.copy())
        df_ranked_2 = ranker.rank_materials(sample_data.copy())
        
        # Rankings should be identical
        assert df_ranked_1['rank'].equals(df_ranked_2['rank'])
        assert np.allclose(
            df_ranked_1['ranking_score'].values, 
            df_ranked_2['ranking_score'].values
        )


class TestExport:
    """Test export functionality"""
    
    def test_export_csv(self, ranker, sample_data, tmp_path):
        """Test CSV export"""
        df_ranked = ranker.rank_materials(sample_data)
        df_top = ranker.get_top_recommendations(df_ranked, top_n=5)
        
        output_path = tmp_path / "rankings.csv"
        ranker.export_rankings(df_top, str(output_path), format='csv')
        
        assert output_path.exists()
        
        # Verify can read back
        df_loaded = pd.read_csv(output_path)
        assert len(df_loaded) == len(df_top)
    
    def test_export_json(self, ranker, sample_data, tmp_path):
        """Test JSON export"""
        df_ranked = ranker.rank_materials(sample_data)
        df_top = ranker.get_top_recommendations(df_ranked, top_n=5)
        
        output_path = tmp_path / "rankings.json"
        ranker.export_rankings(df_top, str(output_path), format='json')
        
        assert output_path.exists()
        
        # Verify can read back
        df_loaded = pd.read_json(output_path)
        assert len(df_loaded) == len(df_top)


class TestExplanations:
    """Test explanation generation"""
    
    def test_generate_explanation(self, ranker, sample_data):
        """Test explanation generation"""
        df_ranked = ranker.rank_materials(sample_data)
        
        if len(df_ranked) > 0:
            explanation = ranker.generate_explanation(df_ranked.iloc[0])
            
            assert isinstance(explanation, str)
            assert len(explanation) > 0
            assert 'Rank' in explanation
            assert 'score' in explanation


class TestEdgeCases:
    """Test edge cases"""
    
    def test_empty_dataframe(self, ranker):
        """Test handling of empty DataFrame"""
        df_empty = pd.DataFrame()
        df_ranked = ranker.rank_materials(df_empty)
        
        assert len(df_ranked) == 0
    
    def test_single_material(self, ranker, sample_data):
        """Test ranking with single material"""
        df_single = sample_data.head(1).copy()
        df_ranked = ranker.rank_materials(df_single)
        
        if len(df_ranked) > 0:
            assert df_ranked.iloc[0]['rank'] == 1
    
    def test_missing_features(self, ranker):
        """Test handling of missing features"""
        df_minimal = pd.DataFrame({
            'recyclability_percent': [50, 60, 70],
            'material_suitability_score': [40, 50, 60],
            'cost_per_unit_usd': [10, 20, 30],
            'co2_emission_per_kg_estimated': [2, 3, 4],
            'supplier_sustainability_compliance_percent': [70, 80, 90],
            'load_handling_score': [5, 6, 7],
            'moisture_resistance_score': [5, 6, 7],
            'thermal_resistance_score': [5, 6, 7]
        })
        
        # Should handle gracefully
        df_ranked = ranker.rank_materials(df_minimal)
        assert len(df_ranked) >= 0


def test_integration_workflow(sample_data):
    """Integration test of complete workflow"""
    # Initialize ranker
    ranker = MaterialRanker(ranking_mode='balanced')
    
    # Relax constraints
    ranker.constraints['min_recyclability_percent'] = 20.0
    ranker.constraints['max_cost_per_unit'] = 100.0
    
    # Rank materials
    df_ranked = ranker.rank_materials(sample_data)
    assert len(df_ranked) > 0
    
    # Get top recommendations
    df_top = ranker.get_top_recommendations(df_ranked, top_n=10)
    assert len(df_top) <= 10
    
    # Verify top material has highest score
    assert df_top.iloc[0]['rank'] == 1
    assert df_top.iloc[0]['ranking_score'] == df_ranked['ranking_score'].max()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
