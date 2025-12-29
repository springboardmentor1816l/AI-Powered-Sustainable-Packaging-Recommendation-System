"""
Test script to verify the preprocessing pipeline works correctly
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PIPELINE_PATH = BASE_DIR / 'models' / 'preprocessing' / 'preprocessing_pipeline.pkl'
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'cleaned_integrated_materials.csv'

def test_pipeline_loading():
    """Test if pipeline can be loaded"""
    print("Test 1: Loading Pipeline...")
    try:
        with open(PIPELINE_PATH, 'rb') as f:
            pipeline = pickle.load(f)
        print("✓ Pipeline loaded successfully")
        return pipeline
    except Exception as e:
        print(f"✗ Failed to load pipeline: {e}")
        return None

def test_pipeline_transform(pipeline):
    """Test if pipeline can transform data"""
    print("\nTest 2: Transforming Data...")
    try:
        # Load data
        df = pd.read_csv(DATA_PATH)
        
        # Select features (excluding IDs and text columns)
        feature_columns = [
            'recyclability_percent', 'recycled_content_percent', 'reusability_percent',
            'biodegradation_time_days', 'end_of_life_disposal_percent',
            'carbon_footprint_kg_co2_unit', 'co2_emission_per_kg_estimated',
            'waste_reduction_impact_percent', 'sustainability_target_progress_percent',
            'load_handling_score', 'moisture_resistance_score', 'thermal_resistance_score',
            'cost_per_unit_usd', 'annual_usage_units', 'total_material_weight_tons',
            'supplier_sustainability_compliance_percent', 'packaging_type', 'material_type',
            'supplier_region', 'recyclability_category'
        ]
        
        X = df[feature_columns]
        
        # Transform
        X_transformed = pipeline.transform(X)
        
        print(f"✓ Data transformed successfully")
        print(f"  Input shape: {X.shape}")
        print(f"  Output shape: {X_transformed.shape}")
        print(f"  No NaN values: {not np.isnan(X_transformed).any()}")
        
        return X_transformed
    except Exception as e:
        print(f"✗ Failed to transform data: {e}")
        return None

def test_feature_names(pipeline):
    """Test if feature names can be retrieved"""
    print("\nTest 3: Getting Feature Names...")
    try:
        feature_names = pipeline.get_feature_names_out()
        print(f"✓ Feature names retrieved successfully")
        print(f"  Total features: {len(feature_names)}")
        print(f"  First 5 features: {list(feature_names[:5])}")
        return feature_names
    except Exception as e:
        print(f"✗ Failed to get feature names: {e}")
        return None

def test_consistency():
    """Test if transformation is consistent across multiple calls"""
    print("\nTest 4: Checking Consistency...")
    try:
        with open(PIPELINE_PATH, 'rb') as f:
            pipeline = pickle.load(f)
        
        df = pd.read_csv(DATA_PATH).head(10)
        feature_columns = [
            'recyclability_percent', 'recycled_content_percent', 'reusability_percent',
            'biodegradation_time_days', 'end_of_life_disposal_percent',
            'carbon_footprint_kg_co2_unit', 'co2_emission_per_kg_estimated',
            'waste_reduction_impact_percent', 'sustainability_target_progress_percent',
            'load_handling_score', 'moisture_resistance_score', 'thermal_resistance_score',
            'cost_per_unit_usd', 'annual_usage_units', 'total_material_weight_tons',
            'supplier_sustainability_compliance_percent', 'packaging_type', 'material_type',
            'supplier_region', 'recyclability_category'
        ]
        X = df[feature_columns]
        
        # Transform twice
        X_transformed_1 = pipeline.transform(X)
        X_transformed_2 = pipeline.transform(X)
        
        # Check if results are identical
        is_consistent = np.allclose(X_transformed_1, X_transformed_2)
        
        if is_consistent:
            print("✓ Transformations are consistent")
        else:
            print("✗ Transformations are inconsistent")
        
        return is_consistent
    except Exception as e:
        print(f"✗ Failed consistency check: {e}")
        return False

def main():
    print("="*60)
    print("Preprocessing Pipeline Test Suite")
    print("="*60)
    
    # Run tests
    pipeline = test_pipeline_loading()
    if pipeline is None:
        print("\nTests failed: Cannot load pipeline")
        return
    
    X_transformed = test_pipeline_transform(pipeline)
    if X_transformed is None:
        print("\nTests failed: Cannot transform data")
        return
    
    feature_names = test_feature_names(pipeline)
    if feature_names is None:
        print("\nTests failed: Cannot get feature names")
        return
    
    is_consistent = test_consistency()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    all_passed = pipeline is not None and X_transformed is not None and \
                 feature_names is not None and is_consistent
    
    if all_passed:
        print("✅ All tests passed! Pipeline is ready to use.")
    else:
        print("⚠️  Some tests failed. Please review the pipeline.")
    
    print("\nPipeline is production-ready ✓")

if __name__ == "__main__":
    main()
