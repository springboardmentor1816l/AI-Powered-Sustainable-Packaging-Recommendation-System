"""
CSV Validation Script for EcoPackAI Dataset
Validates schema, data types, ranges, and detects anomalies
"""

import pandas as pd
import numpy as np
from pathlib import Path

def validate_csv(file_path):
    """Validate the EcoPackAI dataset CSV file"""
    
    print("="*60)
    print("EcoPackAI Dataset Validation Report")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv(file_path)
    print(f"\n✓ Successfully loaded dataset: {file_path}")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
    
    # Expected columns
    expected_columns = [
        'Material ID', 'Packaging Type', 'Material Type',
        'Suitable Product Categories', 'Recommended Packaging Use Cases',
        'Supplier Region', 'Recyclability (%)', 'Recyclability Category',
        'Recycled Content (%)', 'Reusability (%)', 'Biodegradation Time (days)',
        'End-of-Life Disposal (%)', 'Carbon Footprint (kg CO2/unit)',
        'CO2 Emission per kg (estimated)', 'Waste Reduction Impact (%)',
        'Sustainability Target Progress (%)', 'Load Handling Score',
        'Moisture Resistance Score', 'Thermal Resistance Score',
        'Cost per Unit (USD)', 'Annual Usage (units)',
        'Total Material Weight (tons)', 'Supplier Sustainability Compliance (%)'
    ]
    
    # Schema validation
    print("1. SCHEMA VALIDATION")
    print("-" * 60)
    actual_columns = df.columns.tolist()
    
    if set(expected_columns) == set(actual_columns):
        print("✓ All expected columns present")
    else:
        missing = set(expected_columns) - set(actual_columns)
        extra = set(actual_columns) - set(expected_columns)
        if missing:
            print(f"✗ Missing columns: {missing}")
        if extra:
            print(f"⚠ Extra columns: {extra}")
    
    # Duplicate check
    print("\n2. DUPLICATE ROWS")
    print("-" * 60)
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        print("✓ No duplicate rows found")
    else:
        print(f"⚠ Found {duplicates} duplicate rows ({duplicates/len(df)*100:.2f}%)")
    
    # Missing values
    print("\n3. MISSING VALUES")
    print("-" * 60)
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) == 0:
        print("✓ No missing values")
    else:
        print("⚠ Missing values detected:")
        for col, count in missing_cols.items():
            pct = (count / len(df)) * 100
            print(f"  {col}: {count} ({pct:.1f}%)")
    
    # Data type validation
    print("\n4. DATA TYPE VALIDATION")
    print("-" * 60)
    
    # Percentage columns should be numeric (0-100)
    percentage_cols = [col for col in df.columns if '(%)' in col]
    for col in percentage_cols:
        if df[col].dtype in ['float64', 'int64']:
            valid_range = df[col].dropna().between(0, 100).all()
            if valid_range:
                print(f"✓ {col}: Valid range [0-100]")
            else:
                invalid_values = df[~df[col].between(0, 100)][col].dropna()
                print(f"✗ {col}: Found {len(invalid_values)} values outside [0-100]")
        else:
            print(f"✗ {col}: Expected numeric, got {df[col].dtype}")
    
    # Score columns should be 1-10
    score_cols = ['Load Handling Score', 'Moisture Resistance Score', 'Thermal Resistance Score']
    for col in score_cols:
        if df[col].dtype in ['float64', 'int64']:
            valid_range = df[col].dropna().between(1, 10).all()
            if valid_range:
                print(f"✓ {col}: Valid range [1-10]")
            else:
                invalid_values = df[~df[col].between(1, 10)][col].dropna()
                print(f"✗ {col}: Found {len(invalid_values)} values outside [1-10]")
    
    # Cost should be positive
    cost_col = 'Cost per Unit (USD)'
    if df[cost_col].dtype in ['float64', 'int64']:
        negative_costs = (df[cost_col] < 0).sum()
        if negative_costs == 0:
            print(f"✓ {cost_col}: All values >= 0")
        else:
            print(f"✗ {cost_col}: Found {negative_costs} negative values")
    
    # Outlier detection using IQR
    print("\n5. OUTLIER DETECTION (IQR Method)")
    print("-" * 60)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_counts = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        if outliers > 0:
            outlier_counts[col] = outliers
    
    if len(outlier_counts) == 0:
        print("✓ No extreme outliers detected")
    else:
        print("⚠ Extreme outliers detected:")
        for col, count in outlier_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {col}: {count} ({pct:.1f}%)")
    
    # Categorical validation
    print("\n6. CATEGORICAL VALIDATION")
    print("-" * 60)
    
    packaging_types = df['Packaging Type'].value_counts()
    print(f"✓ Packaging Type: {len(packaging_types)} categories")
    print(f"  Top 3: {', '.join(packaging_types.head(3).index.tolist())}")
    
    material_types = df['Material Type'].value_counts()
    print(f"✓ Material Type: {len(material_types)} categories")
    print(f"  Top 3: {', '.join(material_types.head(3).index.tolist())}")
    
    regions = df['Supplier Region'].value_counts()
    print(f"✓ Supplier Region: {len(regions)} regions")
    print(f"  Distribution: {', '.join([f'{k}: {v}' for k, v in regions.items()])}")
    
    # Final summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total Records: {len(df)}")
    print(f"Complete Records: {len(df) - df.isnull().any(axis=1).sum()}")
    print(f"Records with Missing Values: {df.isnull().any(axis=1).sum()}")
    print(f"Duplicate Rows: {duplicates}")
    
    if duplicates == 0 and len(missing_cols) == 0:
        print("\n✅ VALIDATION PASSED - Dataset is ready for processing")
    elif len(missing_cols) > 0:
        print("\n⚠️ VALIDATION PASSED WITH WARNINGS - Missing values need handling")
    else:
        print("\n❌ VALIDATION FAILED - Critical issues detected")
    
    return df

if __name__ == "__main__":
    file_path = Path("data/raw/EcoPackAI_dataset.csv")
    
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        exit(1)
    
    df = validate_csv(file_path)
    print("\n✓ Validation complete!")
