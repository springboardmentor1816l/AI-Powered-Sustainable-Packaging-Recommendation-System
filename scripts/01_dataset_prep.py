"""
01_dataset_prep.py
EcoPackAI - Define Target Variables & Features

This script executes the dataset preparation logic from the notebook.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

print("=" * 80)
print("EcoPackAI - Dataset Preparation")
print("=" * 80)

# Define paths
DATA_DIR = Path('data')
MODEL_READY_DIR = DATA_DIR / 'model_ready'
OUTPUT_DIR = DATA_DIR / 'ml_ready'
OUTPUT_DIR.mkdir(exist_ok=True)

# Load the engineered dataset
print("\n1. Loading dataset...")
df = pd.read_csv(MODEL_READY_DIR / 'materials_engineered.csv')
print(f"✅ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Define target variable
TARGET_VARIABLE = 'material_type'
print(f"\n2. Target Variable: {TARGET_VARIABLE}")
print(f"\nTarget Distribution:")
print(df[TARGET_VARIABLE].value_counts())

# Define feature categories
MATERIAL_PROPERTIES = [
    'recyclability_percent',
    'recycled_content_percent',
    'reusability_percent',
    'biodegradation_time_days',
    'end_of_life_disposal_percent',
    'carbon_footprint_kg_co2_unit',
    'co2_emission_per_kg_estimated',
    'waste_reduction_impact_percent',
    'sustainability_target_progress_percent'
]

PACKAGING_REQUIREMENTS = [
    'load_handling_score',
    'moisture_resistance_score',
    'thermal_resistance_score'
]

COST_OPERATIONS = [
    'cost_per_unit_usd',
    'annual_usage_units',
    'total_material_weight_tons',
    'supplier_sustainability_compliance_percent'
]

ENGINEERED_INDICES = [
    'co2_impact_index',
    'cost_efficiency_index',
    'material_suitability_score',
    'overall_sustainability_score'
]

CATEGORICAL_FEATURES = [
    'packaging_type',
    'suitable_product_categories',
    'recommended_packaging_use_cases',
    'supplier_region',
    'recyclability_category'
]

# All numeric features
NUMERIC_FEATURES = (
    MATERIAL_PROPERTIES + 
    PACKAGING_REQUIREMENTS + 
    COST_OPERATIONS + 
    ENGINEERED_INDICES
)

# All features
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

print(f"\n3. Feature Summary:")
print(f"   Material Properties: {len(MATERIAL_PROPERTIES)} features")
print(f"   Packaging Requirements: {len(PACKAGING_REQUIREMENTS)} features")
print(f"   Cost & Operations: {len(COST_OPERATIONS)} features")
print(f"   Engineered Indices: {len(ENGINEERED_INDICES)} features")
print(f"   Categorical Features: {len(CATEGORICAL_FEATURES)} features")
print(f"\n   Total Numeric Features: {len(NUMERIC_FEATURES)}")
print(f"   Total Features: {len(ALL_FEATURES)}")

# Check feature availability
print("\n4. Feature Availability Check:")
missing_features = [feat for feat in ALL_FEATURES if feat not in df.columns]
if missing_features:
    print(f"⚠️  Warning: {len(missing_features)} features not found:")
    for feat in missing_features:
        print(f"   - {feat}")
else:
    print("✅ All features are available in the dataset!")

# Prepare X and y
valid_features = [feat for feat in ALL_FEATURES if feat in df.columns]
X_raw = df[valid_features].copy()
y_raw = df[TARGET_VARIABLE].copy()

print(f"\n5. Features and Target Separated:")
print(f"   X_raw shape: {X_raw.shape}")
print(f"   y_raw shape: {y_raw.shape}")
print(f"   Features used: {len(valid_features)}")
print(f"   Target classes: {y_raw.nunique()}")

# Save data
print(f"\n6. Saving processed data...")
X_raw.to_csv(OUTPUT_DIR / 'X_raw.csv', index=False)
y_raw.to_csv(OUTPUT_DIR / 'y_raw.csv', index=False)
print(f"✅ Saved X_raw.csv: {X_raw.shape}")
print(f"✅ Saved y_raw.csv: {y_raw.shape}")

# Save feature metadata
feature_metadata = {
    'target_variable': TARGET_VARIABLE,
    'total_features': len(valid_features),
    'numeric_features': len([f for f in valid_features if f in NUMERIC_FEATURES]),
    'categorical_features': len([f for f in valid_features if f in CATEGORICAL_FEATURES]),
    'material_properties': MATERIAL_PROPERTIES,
    'packaging_requirements': PACKAGING_REQUIREMENTS,
    'cost_operations': COST_OPERATIONS,
    'engineered_indices': ENGINEERED_INDICES,
    'categorical_features': CATEGORICAL_FEATURES,
    'all_features': valid_features
}

with open(OUTPUT_DIR / 'feature_metadata.json', 'w') as f:
    json.dump(feature_metadata, f, indent=2)

print(f"✅ Saved feature_metadata.json")

# Display summary statistics
print(f"\n7. Data Summary:")
print("\nNumeric Feature Statistics:")
numeric_cols = [col for col in valid_features if col in NUMERIC_FEATURES]
print(X_raw[numeric_cols].describe().T[['mean', 'std', 'min', 'max']])

print("\nCategorical Feature Cardinality:")
categorical_cols = [col for col in valid_features if col in CATEGORICAL_FEATURES]
for col in categorical_cols:
    print(f"   {col}: {X_raw[col].nunique()} unique values")

print("\n" + "=" * 80)
print("✅ DATASET PREPARATION COMPLETE!")
print("=" * 80)
print(f"\nTarget Variable: {TARGET_VARIABLE}")
print(f"Total Features: {len(valid_features)}")
print(f"Dataset Shape: {df.shape}")
print(f"Output Directory: {OUTPUT_DIR}")
print("\n🚀 Ready for next phase: Feature Engineering & Model Training!")
print("=" * 80)
