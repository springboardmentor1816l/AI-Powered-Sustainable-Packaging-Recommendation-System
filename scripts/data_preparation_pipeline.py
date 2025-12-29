"""
EcoPackAI - Complete Data Preparation Pipeline
Following the correct workflow:
1. Preprocess Product dataset → product_cleaned
2. Preprocess Material dataset → material_cleaned
3. Integrate datasets → integrated_dataset
4. Create X_raw & Y_raw

Author: EcoPackAI Team
Date: 2025-12-26
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
ML_READY_DIR = DATA_DIR / 'ml_ready'

# Create directories
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
ML_READY_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print(" " * 20 + "ECOPACKAI - DATA PREPARATION PIPELINE")
print("="*80)
print("\nFollowing the correct workflow:")
print("  Step 1: Preprocess Product dataset → product_cleaned")
print("  Step 2: Preprocess Material dataset → material_cleaned")
print("  Step 3: Integrate datasets → integrated_dataset")
print("  Step 4: Create X_raw & Y_raw")
print("="*80)


# ==============================================================================
# STEP 1: PREPROCESS PRODUCT DATASET
# ==============================================================================

def preprocess_product_dataset():
    """
    Preprocess the product dataset
    - Handle missing values
    - Validate data types
    - Encode categorical fields
    - Normalize numeric features if needed
    
    Returns: product_cleaned DataFrame
    """
    print("\n" + "="*80)
    print("STEP 1: PREPROCESSING PRODUCT DATASET")
    print("="*80)
    
    # Load product dataset
    product_path = DATA_DIR / 'product_dataset.csv'
    print(f"\n📥 Loading product dataset from: {product_path}")
    
    df = pd.read_csv(product_path)
    print(f"✓ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    
    # Display initial info
    print(f"\n📊 Initial Dataset Info:")
    print(f"  - Total products: {len(df)}")
    print(f"  - Missing values: {df.isnull().sum().sum()}")
    
    # Check for missing values
    print(f"\n🔍 Checking for missing values:")
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        print("  Missing values found:")
        for col in missing_counts[missing_counts > 0].index:
            print(f"    - {col}: {missing_counts[col]} ({missing_counts[col]/len(df)*100:.1f}%)")
    else:
        print("  ✓ No missing values found")
    
    # Validate and clean data types
    print(f"\n🔧 Validating data types:")
    
    # Ensure product_id is string
    if 'product_id' in df.columns:
        df['product_id'] = df['product_id'].astype(str)
        print(f"  ✓ product_id: string")
    
    # Ensure product_weight_kg is numeric
    if 'product_weight_kg' in df.columns:
        df['product_weight_kg'] = pd.to_numeric(df['product_weight_kg'], errors='coerce')
        print(f"  ✓ product_weight_kg: numeric")
    
    # Ensure fragility_index is numeric
    if 'fragility_index' in df.columns:
        df['fragility_index'] = pd.to_numeric(df['fragility_index'], errors='coerce')
        print(f"  ✓ fragility_index: numeric")
    
    # Handle categorical fields
    print(f"\n🏷️  Processing categorical fields:")
    
    categorical_cols = ['category', 'shipping_type']
    for col in categorical_cols:
        if col in df.columns:
            # Fill missing categoricals with 'Unknown'
            df[col] = df[col].fillna('Unknown')
            print(f"  ✓ {col}: {df[col].nunique()} unique values")
    
    # Handle missing numeric values
    print(f"\n🔢 Handling missing numeric values:")
    
    numeric_cols = ['product_weight_kg', 'fragility_index']
    for col in numeric_cols:
        if col in df.columns:
            missing_before = df[col].isnull().sum()
            if missing_before > 0:
                # Fill with median
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"  ✓ {col}: Filled {missing_before} missing values with median ({median_val:.2f})")
            else:
                print(f"  ✓ {col}: No missing values")
    
    # Add derived features (useful for integration)
    print(f"\n✨ Creating derived features:")
    
    # Weight category
    if 'product_weight_kg' in df.columns:
        df['weight_category'] = pd.cut(
            df['product_weight_kg'],
            bins=[0, 0.5, 2, 5, float('inf')],
            labels=['Very Light', 'Light', 'Medium', 'Heavy']
        )
        print(f"  ✓ weight_category created")
    
    # Fragility category
    if 'fragility_index' in df.columns:
        df['fragility_category'] = pd.cut(
            df['fragility_index'],
            bins=[0, 2, 3, 4, float('inf')],
            labels=['Low Fragility', 'Medium Fragility', 'High Fragility', 'Very High Fragility']
        )
        print(f"  ✓ fragility_category created")
    
    # Summary statistics
    print(f"\n📊 Product Dataset Summary:")
    print(f"  - Total products after cleaning: {len(df)}")
    print(f"  - Product categories: {df['category'].nunique() if 'category' in df.columns else 'N/A'}")
    print(f"  - Shipping types: {df['shipping_type'].nunique() if 'shipping_type' in df.columns else 'N/A'}")
    print(f"  - Weight range: {df['product_weight_kg'].min():.2f} - {df['product_weight_kg'].max():.2f} kg")
    print(f"  - Fragility range: {df['fragility_index'].min()} - {df['fragility_index'].max()}")
    
    # Save product_cleaned
    output_path = PROCESSED_DIR / 'product_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"\n💾 Saved product_cleaned to: {output_path}")
    
    return df


# ==============================================================================
# STEP 2: PREPROCESS MATERIAL DATASET
# ==============================================================================

def preprocess_material_dataset():
    """
    Preprocess the material dataset
    - Handle missing values
    - Validate sustainability metrics
    - Encode categorical fields
    - Normalize numeric features
    
    Returns: material_cleaned DataFrame
    """
    print("\n" + "="*80)
    print("STEP 2: PREPROCESSING MATERIAL DATASET")
    print("="*80)
    
    # Load material dataset (from the EcoPackAI dataset)
    material_path = RAW_DIR / 'EcoPackAI_dataset.csv'
    print(f"\n📥 Loading material dataset from: {material_path}")
    
    df = pd.read_csv(material_path)
    print(f"✓ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Display initial info
    print(f"\n📊 Initial Dataset Info:")
    print(f"  - Total materials: {len(df)}")
    print(f"  - Missing values: {df.isnull().sum().sum()}")
    
    # Check for missing values
    print(f"\n🔍 Checking for missing values:")
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        print("  Missing values found:")
        for col in missing_counts[missing_counts > 0].index:
            print(f"    - {col}: {missing_counts[col]} ({missing_counts[col]/len(df)*100:.1f}%)")
    else:
        print("  ✓ No missing values found")
    
    # Validate sustainability metrics
    print(f"\n🌱 Validating sustainability metrics:")
    
    sustainability_metrics = [
        'recyclability_percent', 'recycled_content_percent', 'reusability_percent',
        'carbon_footprint_kg_co2_unit', 'co2_emission_per_kg_estimated',
        'waste_reduction_impact_percent'
    ]
    
    for metric in sustainability_metrics:
        if metric in df.columns:
            # Ensure numeric
            df[metric] = pd.to_numeric(df[metric], errors='coerce')
            
            # Check range for percentage fields
            if 'percent' in metric:
                invalid_count = ((df[metric] < 0) | (df[metric] > 100)).sum()
                if invalid_count > 0:
                    # Clip to valid range
                    df[metric] = df[metric].clip(0, 100)
                    print(f"  ⚠ {metric}: Fixed {invalid_count} out-of-range values")
                else:
                    print(f"  ✓ {metric}: Valid range (0-100)")
            else:
                print(f"  ✓ {metric}: {df[metric].min():.2f} - {df[metric].max():.2f}")
    
    # Handle categorical fields
    print(f"\n🏷️  Processing categorical fields:")
    
    categorical_cols = ['packaging_type', 'material_type', 'supplier_region', 'recyclability_category']
    for col in categorical_cols:
        if col in df.columns:
            # Fill missing categoricals
            df[col] = df[col].fillna('Unknown')
            print(f"  ✓ {col}: {df[col].nunique()} unique values")
    
    # Handle missing numeric values
    print(f"\n🔢 Handling missing numeric values:")
    
    numeric_cols = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
    for col in numeric_cols:
        if col in df.columns:
            missing_before = df[col].isnull().sum()
            if missing_before > 0:
                # Fill with median
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"  ✓ {col}: Filled {missing_before} missing values with median ({median_val:.2f})")
    
    # Add derived features for integration
    print(f"\n✨ Creating derived features:")
    
    # Protection capability score (for fragile products)
    if all(col in df.columns for col in ['load_handling_score', 'moisture_resistance_score', 'thermal_resistance_score']):
        df['protection_score'] = (
            df['load_handling_score'] * 0.4 +
            df['moisture_resistance_score'] * 0.3 +
            df['thermal_resistance_score'] * 0.3
        )
        print(f"  ✓ protection_score created (weighted avg of resistance scores)")
    
    # Sustainability index
    if all(col in df.columns for col in ['recyclability_percent', 'waste_reduction_impact_percent']):
        df['sustainability_index'] = (
            df['recyclability_percent'] * 0.5 +
            df['waste_reduction_impact_percent'] * 0.5
        )
        print(f"  ✓ sustainability_index created")
    
    # Summary statistics
    print(f"\n📊 Material Dataset Summary:")
    print(f"  - Total materials after cleaning: {len(df)}")
    print(f"  - Material types: {df['material_type'].nunique() if 'material_type' in df.columns else 'N/A'}")
    print(f"  - Packaging types: {df['packaging_type'].nunique() if 'packaging_type' in df.columns else 'N/A'}")
    print(f"  - Recyclability range: {df['recyclability_percent'].min():.1f}% - {df['recyclability_percent'].max():.1f}%")
    print(f"  - Cost range: ${df['cost_per_unit_usd'].min():.2f} - ${df['cost_per_unit_usd'].max():.2f}")
    
    # Save material_cleaned
    output_path = PROCESSED_DIR / 'material_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"\n💾 Saved material_cleaned to: {output_path}")
    
    return df


# ==============================================================================
# STEP 3: INTEGRATE DATASETS
# ==============================================================================

def integrate_datasets(product_df, material_df):
    """
    Integrate product and material datasets based on compatibility rules
    
    Compatibility criteria:
    - Product category matches suitable product categories
    - Load handling score matches product weight
    - Fragility vs protection scores
    
    Returns: integrated_dataset DataFrame
    """
    print("\n" + "="*80)
    print("STEP 3: INTEGRATING DATASETS")
    print("="*80)
    
    print(f"\n📊 Input datasets:")
    print(f"  - Products: {len(product_df)} rows")
    print(f"  - Materials: {len(material_df)} rows")
    
    # Define compatibility rules
    print(f"\n🔗 Defining compatibility rules:")
    
    # Category mapping
    category_mapping = {
        'Electronics': ['Electronics', 'Fragile Items'],
        'Food': ['Food & Beverage'],
        'Cosmetics': ['Cosmetics'],
        'Pharmacy': ['Pharmaceuticals'],
        'Drinkware': ['Food & Beverage'],
        'Paper Product': ['E-commerce', 'Consumer Goods']
    }
    
    print(f"  ✓ Category compatibility rules defined")
    
    # Weight-based load handling requirements
    def get_min_load_handling(weight):
        """Determine minimum load handling score based on weight"""
        if weight < 0.5:
            return 1
        elif weight < 2:
            return 3
        elif weight < 5:
            return 5
        else:
            return 7
    
    print(f"  ✓ Weight-based load handling rules defined")
    
    # Fragility-based protection requirements
    def get_min_protection_score(fragility):
        """Determine minimum protection score based on fragility"""
        if fragility <= 2:
            return 2
        elif fragility <= 3:
            return 4
        elif fragility <= 4:
            return 6
        else:
            return 7
    
    print(f"  ✓ Fragility-based protection rules defined")
    
    # Create integrated dataset
    print(f"\n🔄 Creating integrated dataset...")
    
    integrated_rows = []
    compatibility_count = 0
    total_combinations = len(product_df) * len(material_df)
    
    print(f"  Evaluating {total_combinations:,} possible combinations...")
    
    for _, product in product_df.iterrows():
        product_category = product.get('category', 'Unknown')
        product_weight = product.get('product_weight_kg', 0)
        product_fragility = product.get('fragility_index', 0)
        
        # Get requirements
        min_load_handling = get_min_load_handling(product_weight)
        min_protection = get_min_protection_score(product_fragility)
        
        # Find compatible materials
        for _, material in material_df.iterrows():
            # Check category compatibility
            suitable_categories = material.get('suitable_product_categories', '')
            
            # Simple category matching (you can make this more sophisticated)
            category_match = False
            if pd.notna(suitable_categories):
                suitable_list = [cat.strip() for cat in str(suitable_categories).split(',')]
                for cat in suitable_list:
                    if product_category in cat or cat in product_category:
                        category_match = True
                        break
            
            # Check load handling compatibility
            material_load_score = material.get('load_handling_score', 0)
            load_compatible = material_load_score >= min_load_handling
            
            # Check protection compatibility
            material_protection = material.get('protection_score', 
                                             material.get('load_handling_score', 0))
            protection_compatible = material_protection >= min_protection
            
            # If compatible, create integrated row
            if category_match and load_compatible and protection_compatible:
                integrated_row = {
                    # Product features
                    'product_id': product.get('product_id'),
                    'product_name': product.get('product_name'),
                    'product_category': product_category,
                    'product_weight_kg': product_weight,
                    'fragility_index': product_fragility,
                    'shipping_type': product.get('shipping_type'),
                    
                    # Material features
                    'material_id': material.get('material_id'),
                    'packaging_type': material.get('packaging_type'),
                    'material_type': material.get('material_type'),
                    'supplier_region': material.get('supplier_region'),
                    
                    # Sustainability features
                    'recyclability_percent': material.get('recyclability_percent'),
                    'recycled_content_percent': material.get('recycled_content_percent'),
                    'reusability_percent': material.get('reusability_percent'),
                    'recyclability_category': material.get('recyclability_category'),
                    
                    # Performance features
                    'load_handling_score': material.get('load_handling_score'),
                    'moisture_resistance_score': material.get('moisture_resistance_score'),
                    'thermal_resistance_score': material.get('thermal_resistance_score'),
                    'protection_score': material.get('protection_score'),
                    
                    # Environmental features
                    'carbon_footprint_kg_co2_unit': material.get('carbon_footprint_kg_co2_unit'),
                    'co2_emission_per_kg_estimated': material.get('co2_emission_per_kg_estimated'),
                    'waste_reduction_impact_percent': material.get('waste_reduction_impact_percent'),
                    
                    # Target variables
                    'cost_per_unit_usd': material.get('cost_per_unit_usd'),
                    
                    # Additional metrics
                    'supplier_sustainability_compliance_percent': material.get('supplier_sustainability_compliance_percent'),
                    'sustainability_index': material.get('sustainability_index'),
                }
                
                integrated_rows.append(integrated_row)
                compatibility_count += 1
    
    # Create DataFrame
    integrated_df = pd.DataFrame(integrated_rows)
    
    print(f"\n✅ Integration complete:")
    print(f"  - Compatible combinations found: {compatibility_count:,}")
    print(f"  - Compatibility rate: {compatibility_count/total_combinations*100:.2f}%")
    print(f"  - Integrated dataset rows: {len(integrated_df)}")
    print(f"  - Integrated dataset columns: {len(integrated_df.columns)}")
    
    # Display sample statistics
    if len(integrated_df) > 0:
        print(f"\n📊 Integrated Dataset Statistics:")
        print(f"  - Unique products: {integrated_df['product_id'].nunique()}")
        print(f"  - Unique materials: {integrated_df['material_id'].nunique()}")
        print(f"  - Average materials per product: {len(integrated_df) / integrated_df['product_id'].nunique():.1f}")
        
        print(f"\n  Distribution by material type:")
        for mat_type, count in integrated_df['material_type'].value_counts().head().items():
            print(f"    - {mat_type}: {count} ({count/len(integrated_df)*100:.1f}%)")
    
    # Save integrated dataset
    output_path = PROCESSED_DIR / 'integrated_dataset.csv'
    integrated_df.to_csv(output_path, index=False)
    print(f"\n💾 Saved integrated_dataset to: {output_path}")
    
    return integrated_df


# ==============================================================================
# STEP 4: CREATE X_RAW & Y_RAW
# ==============================================================================

def create_ml_inputs(integrated_df):
    """
    Split integrated dataset into X_raw (features) and Y_raw (targets)
    
    X_raw: Input features for the model
    Y_raw: Target variables to predict
    
    Returns: X_raw DataFrame, Y_raw DataFrame
    """
    print("\n" + "="*80)
    print("STEP 4: CREATING X_RAW & Y_RAW")
    print("="*80)
    
    print(f"\n📊 Input: integrated_dataset with {len(integrated_df)} rows")
    
    # Define feature columns (X_raw)
    feature_columns = [
        # Product features
        'product_weight_kg',
        'fragility_index',
        'shipping_type',
        'product_category',
        
        # Material features
        'material_type',
        'packaging_type',
        'supplier_region',
        
        # Performance features
        'load_handling_score',
        'moisture_resistance_score',
        'thermal_resistance_score',
        'protection_score',
        
        # Sustainability features
        'recyclability_percent',
        'recycled_content_percent',
        'reusability_percent',
        'recyclability_category',
        'waste_reduction_impact_percent',
        'supplier_sustainability_compliance_percent',
        'sustainability_index',
    ]
    
    # Define target columns (Y_raw)
    target_columns = [
        'cost_per_unit_usd',
        'co2_emission_per_kg_estimated'
    ]
    
    print(f"\n🎯 Defining features and targets:")
    print(f"  - Feature columns (X_raw): {len(feature_columns)}")
    print(f"  - Target columns (Y_raw): {len(target_columns)}")
    
    # Create X_raw
    print(f"\n📥 Creating X_raw (features)...")
    available_features = [col for col in feature_columns if col in integrated_df.columns]
    missing_features = [col for col in feature_columns if col not in integrated_df.columns]
    
    if missing_features:
        print(f"  ⚠ Warning: {len(missing_features)} features not found in integrated dataset:")
        for feat in missing_features:
            print(f"    - {feat}")
    
    X_raw = integrated_df[available_features].copy()
    print(f"  ✓ X_raw created: {X_raw.shape[0]} rows × {X_raw.shape[1]} columns")
    
    # Add product and material IDs for reference (optional)
    if 'product_id' in integrated_df.columns:
        X_raw.insert(0, 'product_id', integrated_df['product_id'])
    if 'material_id' in integrated_df.columns:
        X_raw.insert(1, 'material_id', integrated_df['material_id'])
    
    print(f"\n  Feature columns:")
    for i, col in enumerate(X_raw.columns, 1):
        print(f"    {i:2d}. {col}")
    
    # Create Y_raw
    print(f"\n📥 Creating Y_raw (targets)...")
    available_targets = [col for col in target_columns if col in integrated_df.columns]
    missing_targets = [col for col in target_columns if col not in integrated_df.columns]
    
    if missing_targets:
        print(f"  ⚠ Warning: {len(missing_targets)} targets not found in integrated dataset:")
        for target in missing_targets:
            print(f"    - {target}")
    
    Y_raw = integrated_df[available_targets].copy()
    print(f"  ✓ Y_raw created: {Y_raw.shape[0]} rows × {Y_raw.shape[1]} columns")
    
    print(f"\n  Target columns:")
    for i, col in enumerate(Y_raw.columns, 1):
        print(f"    {i}. {col}")
        print(f"       - Min: {Y_raw[col].min():.4f}")
        print(f"       - Max: {Y_raw[col].max():.4f}")
        print(f"       - Mean: {Y_raw[col].mean():.4f}")
        print(f"       - Median: {Y_raw[col].median():.4f}")
    
    # Save X_raw and Y_raw
    X_path = ML_READY_DIR / 'X_raw.csv'
    Y_path = ML_READY_DIR / 'Y_raw.csv'
    
    X_raw.to_csv(X_path, index=False)
    Y_raw.to_csv(Y_path, index=False)
    
    print(f"\n💾 Saved X_raw to: {X_path}")
    print(f"💾 Saved Y_raw to: {Y_path}")
    
    # Validation
    print(f"\n✅ Validation:")
    print(f"  - X_raw and Y_raw have same number of rows: {len(X_raw) == len(Y_raw)}")
    print(f"  - No overlap between features and targets: {set(X_raw.columns).isdisjoint(set(Y_raw.columns))}")
    print(f"  - No missing values in Y_raw: {Y_raw.isnull().sum().sum() == 0}")
    
    return X_raw, Y_raw


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function"""
    
    # Step 1: Preprocess Product Dataset
    product_cleaned = preprocess_product_dataset()
    
    # Step 2: Preprocess Material Dataset
    material_cleaned = preprocess_material_dataset()
    
    # Step 3: Integrate Datasets
    integrated_dataset = integrate_datasets(product_cleaned, material_cleaned)
    
    # Step 4: Create X_raw & Y_raw
    X_raw, Y_raw = create_ml_inputs(integrated_dataset)
    
    # Final Summary
    print("\n" + "="*80)
    print(" " * 25 + "PIPELINE COMPLETE!")
    print("="*80)
    
    print(f"\n📦 Output Files:")
    print(f"  1. {PROCESSED_DIR / 'product_cleaned.csv'}")
    print(f"  2. {PROCESSED_DIR / 'material_cleaned.csv'}")
    print(f"  3. {PROCESSED_DIR / 'integrated_dataset.csv'}")
    print(f"  4. {ML_READY_DIR / 'X_raw.csv'}")
    print(f"  5. {ML_READY_DIR / 'Y_raw.csv'}")
    
    print(f"\n📊 Final Statistics:")
    print(f"  - Products processed: {len(product_cleaned)}")
    print(f"  - Materials processed: {len(material_cleaned)}")
    print(f"  - Integrated rows created: {len(integrated_dataset)}")
    print(f"  - Feature columns: {len(X_raw.columns)}")
    print(f"  - Target columns: {len(Y_raw.columns)}")
    
    print(f"\n✅ Data preparation pipeline completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
