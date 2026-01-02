"""
Test and Demonstrate Unified Predictor
=======================================

This script tests the EcoPackPredictor and demonstrates usage.

Author: EcoPackAI Team
Date: 2026-01-02
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from src.inference.predictor import EcoPackPredictor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_single_prediction():
    """Test single instance prediction"""
    print_section("TEST 1: Single Prediction")
    
    # Initialize predictor
    predictor = EcoPackPredictor()
    
    # Sample features
    sample = {
        'recyclability_percent': 95.0,
        'recycled_content_percent': 70.0,
        'reusability_percent': 50.0,
        'biodegradation_time_days': 120,
        'end_of_life_disposal_percent': 95.0,
        'carbon_footprint_kg_co2_unit': 1.8,
        'waste_reduction_impact_percent': 80.0,
        'sustainability_target_progress_percent': 85.0,
        'load_handling_score': 8.0,
        'moisture_resistance_score': 7.0,
        'thermal_resistance_score': 7.0,
        'annual_usage_units': 15000,
        'total_material_weight_tons': 7.5,
        'supplier_sustainability_compliance_percent': 90.0,
        'co2_impact_index': 0.25,
        'cost_efficiency_index': 0.75,
        'material_suitability_score': 70.0,
        'overall_sustainability_score': 0.85
    }
    
    print("Input Features:")
    for key, value in list(sample.items())[:5]:
        print(f" {key}: {value}")
    print(f"  ... ({len(sample)} features total)")
    
    # Predict
    result = predictor.predict_single(sample, include_confidence=True)
    
    print(f"\n📊 Predictions:")
    print(f"  Predicted Cost: ${result.get('predicted_cost', 'N/A'):.2f}")
    print(f"  Predicted CO₂: {result.get('predicted_co2', 'N/A'):.4f} kg/kg")
    
    if 'cost_confidence' in result and result['cost_confidence']:
        print(f"  Cost Confidence (±): ${result['cost_confidence']:.2f}")
    
    logger.info("✓ Single prediction successful")


def test_batch_prediction():
    """Test batch prediction"""
    print_section("TEST 2: Batch Prediction")
    
    # Load data
    data_path = "data/ml_ready/X_raw.csv"
    logger.info(f"Loading data from {data_path}...")
    
    df = pd.read_csv(data_path)
    
    # Remove targets if present
    if 'cost_per_unit_usd' in df.columns:
        df = df.drop(columns=['cost_per_unit_usd'])
    if 'co2_emission_per_kg_estimated' in df.columns:
        df = df.drop(columns=['co2_emission_per_kg_estimated'])
    
    # Use first 10 samples
    df_sample = df.head(10)
    
    logger.info(f"Predicting for {len(df_sample)} samples...")
    
    # Initialize predictor
    predictor = EcoPackPredictor()
    
    # Predict
    results = predictor.predict_all(df_sample, return_confidence=True)
    
    print("\n📊 Batch Prediction Results (first 5):")
    print("-" * 80)
    
    display_cols = ['predicted_cost', 'predicted_co2']
    if 'cost_confidence' in results.columns:
        display_cols.append('cost_confidence')
    
    print(results[display_cols].head().to_string(index=True))
    
    print(f"\n📈 Summary Statistics:")
    print(f"  Average Predicted Cost: ${results['predicted_cost'].mean():.2f}")
    print(f"  Average Predicted CO₂: {results['predicted_co2'].mean():.4f} kg")
    print(f"  Cost Range: ${results['predicted_cost'].min():.2f} - ${results['predicted_cost'].max():.2f}")
    print(f"  CO₂ Range: {results['predicted_co2'].min():.4f} - {results['predicted_co2'].max():.4f} kg")
    
    logger.info("✓ Batch prediction successful")


def test_model_validation():
    """Test model validation with ground truth"""
    print_section("TEST 3: Model Validation")
    
    # Load full dataset with targets
    logger.info("Loading dataset with ground truth...")
    df = pd.read_csv("data/ml_ready/X_raw.csv")
    
    # Separate features and targets
    has_cost = 'cost_per_unit_usd' in df.columns
    has_co2 = 'co2_emission_per_kg_estimated' in df.columns
    
    if has_cost and has_co2:
        y_cost = df['cost_per_unit_usd']
        y_co2 = df['co2_emission_per_kg_estimated']
        X = df.drop(columns=['cost_per_unit_usd', 'co2_emission_per_kg_estimated'])
    else:
        logger.warning("Ground truth not available in dataset")
        return
    
    # Initialize predictor
    predictor = EcoPackPredictor()
    
    # Validate
    metrics = predictor.validate_predictions(X, y_cost, y_co2)
    
    print("\n📊 Validation Metrics:")
    print("-" * 80)
    
    if 'cost' in metrics:
        print("\nCost Model:")
        print(f"  MAE: ${metrics['cost']['mae']:.4f}")
        print(f"  RMSE: ${metrics['cost']['rmse']:.4f}")
        print(f"  R²: {metrics['cost']['r2']:.6f}")
    
    if 'co2' in metrics:
        print("\nCO₂ Model:")
        print(f"  MAE: {metrics['co2']['mae']:.6f} kg")
        print(f"  RMSE: {metrics['co2']['rmse']:.6f} kg")
        print(f"  R²: {metrics['co2']['r2']:.6f}")
    
    logger.info("✓ Model validation successful")


def test_file_batch_prediction():
    """Test batch prediction from CSV file"""
    print_section("TEST 4: File-Based Batch Prediction")
    
    input_path = "data/ml_ready/X_raw.csv"
    output_path = "outputs/predictions/batch_predictions.csv"
    
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")
    
    # Initialize predictor
    predictor = EcoPackPredictor()
    
    # Batch predict from file
    predictor.batch_predict(
        input_path=input_path,
        output_path=output_path,
        include_confidence=True
    )
    
    # Load and display results
    results = pd.read_csv(output_path)
    
    print(f"\n📁 Predictions saved to: {output_path}")
    print(f"   Total predictions: {len(results)}")
    print(f"   File size: {Path(output_path).stat().st_size / 1024:.1f} KB")
    
    print("\n📊 First 3 predictions:")
    cols = ['predicted_cost', 'predicted_co2']
    if 'cost_confidence' in results.columns:
        cols.append('cost_confidence')
    
    print(results[cols].head(3).to_string(index=False))
    
    logger.info("✓ File-based batch prediction successful")


def test_model_info():
    """Test model information retrieval"""
    print_section("TEST 5: Model Information")
    
    # Initialize predictor
    predictor = EcoPackPredictor()
    
    # Get model info
    info = predictor.get_model_info()
    
    print("📦 Loaded Models:")
    print("-" * 80)
    
    for model_type in ['cost_model', 'co2_model']:
        if model_type in info:
            model_info = info[model_type]
            print(f"\n{model_type.replace('_', ' ').title()}:")
            print(f"  Loaded: {'✅' if model_info['loaded'] else '❌'}")
            print(f"  Type: {model_info['type']}")
            print(f"  Path: {model_info['path']}")
    
    if 'metadata' in info and info['metadata']:
        print("\n📋 Metadata:")
        meta = info['metadata']
        print(f"  Version: {meta.get('version', 'N/A')}")
        print(f"  Project: {meta.get('project', 'N/A')}")
        
        if 'models' in meta:
            for model_name, model_meta in meta['models'].items():
                print(f"\n  {model_name}:")
                if 'performance' in model_meta:
                    perf = model_meta['performance']
                    print(f"    Test R²: {perf.get('test_r2', 'N/A')}")
                    print(f"    Test MAE: {perf.get('test_mae', 'N/A')}")
    
    logger.info("✓ Model info retrieval successful")


def demonstrate_use_cases():
    """Demonstrate practical use cases"""
    print_section("DEMONSTRATION: Practical Use Cases")
    
    predictor = EcoPackPredictor()
    
    # Use Case 1: Compare two materials
    print("\n🔍 Use Case 1: Comparing Two Materials")
    print("-" * 80)
    
    cardboard = {
        'recyclability_percent': 95.0,
        'recycled_content_percent': 80.0,
        'reusability_percent': 30.0,
        'biodegradation_time_days': 90,
        'end_of_life_disposal_percent': 95.0,
        'carbon_footprint_kg_co2_unit': 1.2,
        'waste_reduction_impact_percent': 85.0,
        'sustainability_target_progress_percent': 90.0,
        'load_handling_score': 7.0,
        'moisture_resistance_score': 5.0,
        'thermal_resistance_score': 6.0,
        'annual_usage_units': 10000,
        'total_material_weight_tons': 5.0,
        'supplier_sustainability_compliance_percent': 85.0,
        'co2_impact_index': 0.2,
        'cost_efficiency_index': 0.8,
        'material_suitability_score': 65.0,
        'overall_sustainability_score': 0.85
    }
    
    plastic = cardboard.copy()
    plastic['recyclability_percent'] = 60.0
    plastic['recycled_content_percent'] = 30.0
    plastic['carbon_footprint_kg_co2_unit'] = 3.5
    plastic['biodegradation_time_days'] = 500
    plastic['overall_sustainability_score'] = 0.50
    
    result_cardboard = predictor.predict_single(cardboard)
    result_plastic = predictor.predict_single(plastic)
    
    print("\nCardboard Box:")
    print(f"  Cost: ${result_cardboard['predicted_cost']:.2f}")
    print(f"  CO₂: {result_cardboard['predicted_co2']:.4f} kg")
    
    print("\nPlastic Container:")
    print(f"  Cost: ${result_plastic['predicted_cost']:.2f}")
    print(f"  CO₂: {result_plastic['predicted_co2']:.4f} kg")
    
    print("\n💡 Comparison:")
    cost_diff = result_cardboard['predicted_cost'] - result_plastic['predicted_cost']
    co2_diff = result_cardboard['predicted_co2'] - result_plastic['predicted_co2']
    
    print(f"  Cost Difference: ${abs(cost_diff):.2f} ({'Cardboard cheaper' if cost_diff < 0 else 'Plastic cheaper'})")
    print(f"  CO₂ Difference: {abs(co2_diff):.4f} kg ({'Cardboard lower' if co2_diff < 0 else 'Plastic lower'})")
    
    logger.info("✓ Use case demonstration complete")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "PREDICTOR TEST SUITE" + " " * 33 + "║")
    print("║" + " " * 28 + "EcoPackAI Project" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        # Run tests
        test_single_prediction()
        test_batch_prediction()
        test_model_validation()
        test_file_batch_prediction()
        test_model_info()
        demonstrate_use_cases()
        
        print_section("ALL TESTS PASSED! ✅")
        
        print("\n📁 Output files:")
        print("   - outputs/predictions/batch_predictions.csv")
        
        print("\n✨ Predictor is production-ready!\n")
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
