"""
Data Quality Tests for EcoPackAI
Pytest unit tests for validating data integrity
"""

import pandas as pd
import pytest
from pathlib import Path

# Load engineered dataset for testing
@pytest.fixture
def engineered_data():
    """Load engineered dataset"""
    df = pd.read_csv("data/model_ready/materials_engineered.csv")
    return df

def test_no_missing_required_fields(engineered_data):
    """Test that required fields have no missing values"""
    required_fields = [
        'material_id', 'packaging_type', 'material_type',
        'recyclability_percent', 'co2_emission_per_kg_estimated'
    ]
    
    for field in required_fields:
        assert engineered_data[field].notna().all(), f"Missing values found in {field}"

def test_unique_material_ids(engineered_data):
    """Test that material IDs are unique"""
    assert engineered_data['material_id'].is_unique, "Duplicate material IDs found"

def test_percentage_ranges(engineered_data):
    """Test that percentage columns are in valid 0-100 range"""
    percentage_cols = [col for col in engineered_data.columns if 'percent' in col]
    
    for col in percentage_cols:
        values = engineered_data[col].dropna()
        assert values.between(0, 100).all(), f"{col} has values outside [0, 100]"

def test_positive_costs(engineered_data):
    """Test that cost values are non-negative"""
    assert (engineered_data['cost_per_unit_usd'] >= 0).all(), "Negative costs found"

def test_valid_categories(engineered_data):
    """Test that categorical fields have valid values"""
    # Check packaging types
    valid_packaging = ['Cardboard Boxes', 'Protective Fillers (Paper/Biodegradable)',
                      'Steel Racks & Containers', 'Foldable & Stackable Containers',
                      'Plastic Totes & Pallets', 'Bubble Wrap (Minimal Use)']
    assert engineered_data['packaging_type'].isin(valid_packaging).all(), "Invalid packaging type found"

def test_score_ranges(engineered_data):
    """Test that score columns are in valid 1-10 range"""
    score_cols = ['load_handling_score', 'moisture_resistance_score', 'thermal_resistance_score']
    
    for col in score_cols:
        values = engineered_data[col].dropna()
        assert values.between(1, 10).all(), f"{col} has values outside [1, 10]"

def test_feature_engineering_ranges(engineered_data):
    """Test that engineered features are in valid 0-100 range"""
    engineered_features = [
        'co2_impact_index',
        'cost_efficiency_index',
        'material_suitability_score',
        'overall_sustainability_score'
    ]
    
    for feature in engineered_features:
        values = engineered_data[feature].dropna()
        assert values.between(0, 100).all(), f"{feature} has values outside [0, 100]"
        assert len(values) > 0, f"{feature} has no values"

def test_no_duplicates(engineered_data):
    """Test that there are no duplicate rows"""
    assert engineered_data.duplicated().sum() == 0, "Duplicate rows found"

def test_dataset_shape(engineered_data):
    """Test that dataset has expected shape"""
    assert len(engineered_data) > 400, "Dataset has fewer than 400 rows"
    assert len(engineered_data.columns) >= 27, "Dataset missing expected columns"

def test_no_infinite_values(engineered_data):
    """Test that there are no infinite values in numeric columns"""
    numeric_cols = engineered_data.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numeric_cols:
        assert not engineered_data[col].isin([float('inf'), float('-inf')]).any(), f"Infinite values in {col}"
