"""
Handle Missing Values - EcoPackAI
Impute missing values using appropriate strategies
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.impute import SimpleImputer
import joblib

def handle_missing_values(input_path, output_path):
    """Impute missing values in the dataset"""
    
    print("="*60)
    print("Missing Value Imputation")
    print("="*60)
    
    # Load cleaned dataset
    df = pd.read_csv(input_path)
    print(f"\n✓ Loaded dataset: {df.shape}")
    
    # Check missing values
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    
    if len(missing_cols) == 0:
        print("\n✓ No missing values found!")
        df.to_csv(output_path, index=False)
        return df
    
    print(f"\nMissing values in {len(missing_cols)} columns:")
    for col, count in missing_cols.items():
        print(f"  {col}: {count} ({count/len(df)*100:.1f}%)")
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Impute numeric columns with median
    print("\n1. IMPUTING NUMERIC COLUMNS (Median Strategy)")
    print("-" * 60)
    numeric_missing = [col for col in missing_cols.index if col in numeric_cols]
    
    if len(numeric_missing) > 0:
        imputer_numeric = SimpleImputer(strategy='median')
        df[numeric_missing] = imputer_numeric.fit_transform(df[numeric_missing])
        print(f"✓ Imputed {len(numeric_missing)} numeric columns")
        
        # Save imputer
        joblib.dump(imputer_numeric, 'models/encoders/numeric_imputer.pkl')
    else:
        print("✓ No numeric columns with missing values")
    
    # Impute categorical columns with most frequent
    print("\n2. IMPUTING CATEGORICAL COLUMNS (Mode Strategy)")
    print("-" * 60)
    categorical_missing = [col for col in missing_cols.index if col in categorical_cols]
    
    if len(categorical_missing) > 0:
        imputer_categorical = SimpleImputer(strategy='most_frequent')
        df[categorical_missing] = imputer_categorical.fit_transform(df[categorical_missing].values.reshape(-1, len(categorical_missing)))
        print(f"✓ Imputed {len(categorical_missing)} categorical columns")
        
        # Save imputer
        joblib.dump(imputer_categorical, 'models/encoders/categorical_imputer.pkl')
    else:
        print("✓ No categorical columns with missing values")
    
    # Verify no missing values remain
    remaining_missing = df.isnull().sum().sum()
    if remaining_missing == 0:
        print(f"\n✅ All missing values imputed successfully!")
    else:
        print(f"\n⚠️ Warning: {remaining_missing} missing values remain")
    
    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    input_path = Path("data/processed/cleaned_materials.csv")
    output_path = Path("data/processed/cleaned_integrated_materials.csv")
    
    df = handle_missing_values(input_path, output_path)
    print(f"\n✓ Final shape: {df.shape}")
