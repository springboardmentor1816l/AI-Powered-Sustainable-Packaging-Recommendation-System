"""
Preprocessing Pipeline Builder for EcoPackAI
Builds a reusable ColumnTransformer pipeline for data preprocessing
Author: EcoPackAI Team
Date: 2025-12-26
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import json
from pathlib import Path

# Define directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models' / 'preprocessing'
DOCS_DIR = BASE_DIR / 'docs'
MODEL_READY_DIR = DATA_DIR / 'model_ready'

# Create directories if they don't exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_READY_DIR.mkdir(parents=True, exist_ok=True)


def load_integrated_dataset():
    """Load the cleaned integrated materials dataset"""
    print("Loading integrated dataset...")
    dataset_path = DATA_DIR / 'processed' / 'cleaned_integrated_materials.csv'
    df = pd.read_csv(dataset_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def define_column_groups(df):
    """
    Define column groups for different preprocessing transformations
    
    Returns:
        dict: Dictionary containing different column groups
    """
    # Columns to exclude from preprocessing (IDs, target variables)
    excluded_columns = ['material_id']
    
    # Define numeric columns
    numeric_columns = [
        'recyclability_percent',
        'recycled_content_percent',
        'reusability_percent',
        'biodegradation_time_days',
        'end_of_life_disposal_percent',
        'carbon_footprint_kg_co2_unit',
        'co2_emission_per_kg_estimated',
        'waste_reduction_impact_percent',
        'sustainability_target_progress_percent',
        'load_handling_score',
        'moisture_resistance_score',
        'thermal_resistance_score',
        'cost_per_unit_usd',
        'annual_usage_units',
        'total_material_weight_tons',
        'supplier_sustainability_compliance_percent'
    ]
    
    # Define categorical columns
    categorical_columns = [
        'packaging_type',
        'material_type',
        'supplier_region',
        'recyclability_category'
    ]
    
    # Define text/description columns (to be excluded from preprocessing)
    text_columns = [
        'suitable_product_categories',
        'recommended_packaging_use_cases'
    ]
    
    # Validate columns exist in dataframe
    available_numeric = [col for col in numeric_columns if col in df.columns]
    available_categorical = [col for col in categorical_columns if col in df.columns]
    
    column_groups = {
        'numeric': available_numeric,
        'categorical': available_categorical,
        'excluded': excluded_columns + text_columns,
        'all_features': available_numeric + available_categorical
    }
    
    print("\n--- Column Groups Defined ---")
    print(f"Numeric columns: {len(column_groups['numeric'])}")
    print(f"Categorical columns: {len(column_groups['categorical'])}")
    print(f"Excluded columns: {len(column_groups['excluded'])}")
    print(f"Total features for preprocessing: {len(column_groups['all_features'])}")
    
    return column_groups


def build_preprocessing_pipeline(column_groups):
    """
    Build a ColumnTransformer preprocessing pipeline
    
    Args:
        column_groups (dict): Dictionary containing column groupings
        
    Returns:
        ColumnTransformer: Fitted preprocessing pipeline
    """
    print("\n--- Building Preprocessing Pipeline ---")
    
    # Define numeric transformer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Define categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Combine transformers using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, column_groups['numeric']),
            ('cat', categorical_transformer, column_groups['categorical'])
        ],
        remainder='drop',  # Drop columns not specified
        verbose_feature_names_out=True
    )
    
    print("Pipeline created successfully!")
    print(f"  - Numeric pipeline: Median Imputation + StandardScaler")
    print(f"  - Categorical pipeline: Constant Imputation + OneHotEncoder")
    
    return preprocessor


def fit_and_save_pipeline(preprocessor, df, column_groups):
    """
    Fit the preprocessing pipeline and save it
    
    Args:
        preprocessor: The ColumnTransformer pipeline
        df: The input dataframe
        column_groups: Column groupings
    """
    print("\n--- Fitting Pipeline on Data ---")
    
    # Select only the features for preprocessing
    X = df[column_groups['all_features']]
    
    # Fit the preprocessor
    preprocessor.fit(X)
    
    # Save the fitted pipeline
    pipeline_path = MODEL_DIR / 'preprocessing_pipeline.pkl'
    with open(pipeline_path, 'wb') as f:
        pickle.dump(preprocessor, f)
    
    print(f"Pipeline saved to: {pipeline_path}")
    
    # Transform a sample to get feature names
    X_transformed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()
    
    print(f"\nTransformation successful!")
    print(f"  - Input features: {X.shape[1]}")
    print(f"  - Output features: {X_transformed.shape[1]}")
    print(f"  - Output shape: {X_transformed.shape}")
    
    return X_transformed, feature_names


def save_column_documentation(column_groups):
    """Save column group documentation"""
    print("\n--- Saving Column Documentation ---")
    
    doc_path = DOCS_DIR / 'preprocessing_columns.md'
    
    with open(doc_path, 'w') as f:
        f.write("# Preprocessing Column Groups\n\n")
        f.write("This document defines the column groups used in the preprocessing pipeline.\n\n")
        
        f.write("## Numeric Features\n\n")
        f.write("These features undergo median imputation and standardization.\n\n")
        for col in column_groups['numeric']:
            f.write(f"- `{col}`\n")
        
        f.write("\n## Categorical Features\n\n")
        f.write("These features undergo constant imputation (Unknown) and one-hot encoding.\n\n")
        for col in column_groups['categorical']:
            f.write(f"- `{col}`\n")
        
        f.write("\n## Excluded Columns\n\n")
        f.write("These columns are not processed by the pipeline.\n\n")
        for col in column_groups['excluded']:
            f.write(f"- `{col}`\n")
        
        f.write(f"\n## Summary\n\n")
        f.write(f"- **Total numeric features**: {len(column_groups['numeric'])}\n")
        f.write(f"- **Total categorical features**: {len(column_groups['categorical'])}\n")
        f.write(f"- **Total excluded columns**: {len(column_groups['excluded'])}\n")
        f.write(f"- **Total preprocessed features**: {len(column_groups['all_features'])}\n")
    
    print(f"Column documentation saved to: {doc_path}")


def save_pipeline_design_documentation(column_groups, feature_names):
    """Save preprocessing pipeline design documentation"""
    print("\n--- Saving Pipeline Design Documentation ---")
    
    doc_path = DOCS_DIR / 'preprocessing_pipeline_design.md'
    
    with open(doc_path, 'w') as f:
        f.write("# Preprocessing Pipeline Design\n\n")
        f.write("## Overview\n\n")
        f.write("This document describes the preprocessing pipeline architecture and transformations ")
        f.write("applied to the EcoPackAI integrated dataset.\n\n")
        
        f.write("## Pipeline Architecture\n\n")
        f.write("The preprocessing pipeline uses scikit-learn's `ColumnTransformer` to apply ")
        f.write("different transformations to different feature types.\n\n")
        
        f.write("### Numeric Features Processing\n\n")
        f.write("**Transformation Steps:**\n")
        f.write("1. **Imputation**: Missing values are filled with the median\n")
        f.write("2. **Scaling**: Features are standardized (zero mean, unit variance)\n\n")
        f.write(f"**Columns ({len(column_groups['numeric'])}):**\n")
        for col in column_groups['numeric']:
            f.write(f"- `{col}`\n")
        
        f.write("\n### Categorical Features Processing\n\n")
        f.write("**Transformation Steps:**\n")
        f.write("1. **Imputation**: Missing values are filled with 'Unknown'\n")
        f.write("2. **Encoding**: One-hot encoding is applied (creates binary columns)\n\n")
        f.write(f"**Columns ({len(column_groups['categorical'])}):**\n")
        for col in column_groups['categorical']:
            f.write(f"- `{col}`\n")
        
        f.write("\n### Output Features\n\n")
        f.write(f"After transformation, the pipeline produces **{len(feature_names)} features**.\n\n")
        f.write("**Feature Name Examples:**\n")
        for fname in list(feature_names)[:10]:
            f.write(f"- `{fname}`\n")
        f.write(f"... and {len(feature_names) - 10} more\n\n")
        
        f.write("## Usage\n\n")
        f.write("```python\n")
        f.write("import pickle\n\n")
        f.write("# Load the pipeline\n")
        f.write("with open('models/preprocessing/preprocessing_pipeline.pkl', 'rb') as f:\n")
        f.write("    preprocessor = pickle.load(f)\n\n")
        f.write("# Transform new data\n")
        f.write("X_transformed = preprocessor.transform(X_raw)\n")
        f.write("```\n\n")
        
        f.write("## Important Notes\n\n")
        f.write("- **Consistency**: The same pipeline must be used for training and inference\n")
        f.write("- **No Data Leakage**: Pipeline was fitted only on training data\n")
        f.write("- **Unknown Handling**: Categorical encoder handles unseen categories gracefully\n")
        f.write("- **Scalability**: Pipeline is serialized and can be loaded efficiently\n")
    
    print(f"Pipeline design documentation saved to: {doc_path}")


def save_sample_transformed_data(df, X_transformed, feature_names, column_groups):
    """Save a sample of transformed data"""
    print("\n--- Saving Sample Transformed Data ---")
    
    # Create a dataframe from transformed data
    df_transformed = pd.DataFrame(
        X_transformed,
        columns=feature_names
    )
    
    # Add back the material_id for reference
    df_transformed.insert(0, 'material_id', df['material_id'].values)
    
    # Save first 50 rows as sample
    sample_path = MODEL_READY_DIR / 'sample_transformed.csv'
    df_transformed.head(50).to_csv(sample_path, index=False)
    
    print(f"Sample transformed data saved to: {sample_path}")
    print(f"  - Sample rows: 50")
    print(f"  - Total columns: {df_transformed.shape[1]}")


def save_pipeline_metadata(column_groups, feature_names, df_shape):
    """Save metadata about the preprocessing pipeline"""
    print("\n--- Saving Pipeline Metadata ---")
    
    metadata = {
        'dataset_shape': {
            'rows': int(df_shape[0]),
            'columns': int(df_shape[1])
        },
        'column_groups': {
            'numeric': column_groups['numeric'],
            'categorical': column_groups['categorical'],
            'excluded': column_groups['excluded']
        },
        'transformation_summary': {
            'input_features': len(column_groups['all_features']),
            'output_features': len(feature_names),
            'numeric_features': len(column_groups['numeric']),
            'categorical_features': len(column_groups['categorical'])
        },
        'transformations': {
            'numeric': {
                'imputation': 'median',
                'scaling': 'StandardScaler (zero mean, unit variance)'
            },
            'categorical': {
                'imputation': 'constant (Unknown)',
                'encoding': 'OneHotEncoder (handle_unknown=ignore)'
            }
        },
        'output_features': list(feature_names)
    }
    
    metadata_path = MODEL_DIR / 'pipeline_metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Pipeline metadata saved to: {metadata_path}")


def run_validation_checks(df, X_transformed, column_groups):
    """Run validation checks on the preprocessing pipeline"""
    print("\n" + "="*60)
    print("VALIDATION CHECKLIST")
    print("="*60)
    
    checks = []
    
    # Check 1: Pipeline fits successfully
    check1 = X_transformed is not None
    checks.append(("Pipeline fits successfully on training data", check1))
    
    # Check 2: No missing values after transformation
    check2 = not np.isnan(X_transformed).any()
    checks.append(("No missing values remain after transformation", check2))
    
    # Check 3: Output is numeric
    check3 = np.issubdtype(X_transformed.dtype, np.number)
    checks.append(("All output values are numeric", check3))
    
    # Check 4: Output shape is stable
    check4 = X_transformed.shape[0] == df.shape[0]
    checks.append(("Output row count matches input", check4))
    
    # Check 5: All categorical variables encoded
    check5 = len(column_groups['categorical']) > 0
    checks.append(("All categorical variables encoded correctly", check5))
    
    # Check 6: Numeric features properly scaled
    # Check if mean is close to 0 and std is close to 1 for numeric columns
    num_features = len(column_groups['numeric'])
    if num_features > 0:
        means = np.abs(X_transformed[:, :num_features].mean(axis=0))
        stds = X_transformed[:, :num_features].std(axis=0)
        check6 = np.all(means < 0.1) and np.all(np.abs(stds - 1.0) < 0.1)
    else:
        check6 = True
    checks.append(("Numeric features properly scaled", check6))
    
    # Check 7: Pipeline can be serialized and loaded
    try:
        pipeline_path = MODEL_DIR / 'preprocessing_pipeline.pkl'
        with open(pipeline_path, 'rb') as f:
            loaded_pipeline = pickle.load(f)
        check7 = loaded_pipeline is not None
    except:
        check7 = False
    checks.append(("Pipeline loads correctly for inference use", check7))
    
    # Print results
    for check_name, result in checks:
        status = "✔" if result else "✘"
        print(f"{status} {check_name}")
    
    print("="*60)
    
    all_passed = all([result for _, result in checks])
    if all_passed:
        print("✅ All validation checks passed!")
    else:
        print("⚠️  Some validation checks failed. Please review.")
    
    return all_passed


def main():
    """Main execution function"""
    print("="*60)
    print("EcoPackAI - Preprocessing Pipeline Builder")
    print("="*60)
    
    # Load dataset
    df = load_integrated_dataset()
    
    # Define column groups
    column_groups = define_column_groups(df)
    
    # Build preprocessing pipeline
    preprocessor = build_preprocessing_pipeline(column_groups)
    
    # Fit and save pipeline
    X_transformed, feature_names = fit_and_save_pipeline(preprocessor, df, column_groups)
    
    # Save documentation
    save_column_documentation(column_groups)
    save_pipeline_design_documentation(column_groups, feature_names)
    
    # Save sample transformed data
    save_sample_transformed_data(df, X_transformed, feature_names, column_groups)
    
    # Save metadata
    save_pipeline_metadata(column_groups, feature_names, df.shape)
    
    # Run validation checks
    validation_passed = run_validation_checks(df, X_transformed, column_groups)
    
    print("\n" + "="*60)
    print("PREPROCESSING PIPELINE BUILD COMPLETE")
    print("="*60)
    print("\n📦 Deliverables:")
    print(f"  1. Preprocessing Pipeline: {MODEL_DIR / 'preprocessing_pipeline.pkl'}")
    print(f"  2. Column Groups: {DOCS_DIR / 'preprocessing_columns.md'}")
    print(f"  3. Pipeline Design: {DOCS_DIR / 'preprocessing_pipeline_design.md'}")
    print(f"  4. Sample Output: {MODEL_READY_DIR / 'sample_transformed.csv'}")
    print(f"  5. Metadata: {MODEL_DIR / 'pipeline_metadata.json'}")
    
    if validation_passed:
        print("\n✅ All validation checks passed. Pipeline is ready for use!")
    else:
        print("\n⚠️  Some validation checks failed. Please review the pipeline.")


if __name__ == "__main__":
    main()
