"""
Data Cleaning Script for EcoPackAI Dataset
Removes incomplete rows, standardizes formatting, handles anomalies
"""

import pandas as pd
import numpy as np
from pathlib import Path

def clean_dataset(input_path, output_path):
    """Clean the EcoPackAI dataset"""
    
    print("="*60)
    print("EcoPackAI Dataset Cleaning")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv(input_path)
    print(f"\n✓ Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    
    initial_rows = len(df)
    
    # 1. Remove rows with excessive missing values (e.g., >50% columns missing)
    print("\n1. REMOVING INCOMPLETE ROWS")
    print("-" * 60)
    threshold = df.shape[1] * 0.5
    df_cleaned = df.dropna(thresh=threshold)
    removed = initial_rows - len(df_cleaned)
    if removed > 0:
        print(f"✓ Removed {removed} rows with >50% missing values")
    else:
        print("✓ No incomplete rows to remove")
    
    # 2. Standardize column names to snake_case
    print("\n2. STANDARDIZING COLUMN NAMES")
    print("-" * 60)
    df_cleaned.columns = (df_cleaned.columns
                          .str.lower()
                          .str.replace(' ', '_')
                          .str.replace('(%)', 'percent')
                          .str.replace('(', '')
                          .str.replace(')', '')
                          .str.replace('/', '_')
                          .str.replace('-', '_'))
    print(f"✓ Standardized {len(df_cleaned.columns)} column names to snake_case")
    
    # 3. Remove duplicate rows
    print("\n3. REMOVING DUPLICATES")
    print("-" * 60)
    before_dedup = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()
    duplicates_removed = before_dedup - len(df_cleaned)
    if duplicates_removed > 0:
        print(f"✓ Removed {duplicates_removed} duplicate rows")
    else:
        print("✓ No duplicate rows found")
    
    # 4. Trim whitespace from string columns
    print("\n4. TRIMMING WHITESPACE")
    print("-" * 60)
    string_cols = df_cleaned.select_dtypes(include=['object']).columns
    for col in string_cols:
        df_cleaned[col] = df_cleaned[col].str.strip() if df_cleaned[col].dtype == 'object' else df_cleaned[col]
    print(f"✓ Trimmed whitespace from {len(string_cols)} text columns")
    
    # 5. Fix data type issues
    print("\n5. FIXING DATA TYPES")
    print("-" * 60)
    
    # Convert numeric columns
    numeric_cols = [col for col in df_cleaned.columns if 
                   'percent' in col or 'score' in col or 'cost' in col or 
                   'weight' in col or 'usage' in col or 'footprint' in col or 
                   'emission' in col or 'time' in col or 'disposal' in col]
    
    for col in numeric_cols:
        try:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
        except:
            pass
    
    print(f"✓ Converted {len(numeric_cols)} columns to numeric types")
    
    # 6. Save cleaned dataset
    print("\n6. SAVING CLEANED DATASET")
    print("-" * 60)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    print(f"✓ Saved to: {output_path}")
    
    # Summary
    print("\n" + "="*60)
    print("CLEANING SUMMARY")
    print("="*60)
    print(f"Original rows: {initial_rows}")
    print(f"Cleaned rows: {len(df_cleaned)}")
    print(f"Rows removed: {initial_rows - len(df_cleaned)}")
    print(f"Data reduction: {(initial_rows - len(df_cleaned))/initial_rows*100:.2f}%")
    print(f"\n✅ Cleaning complete!")
    
    return df_cleaned

if __name__ == "__main__":
    input_path = Path("data/raw/EcoPackAI_dataset.csv")
    output_path = Path("data/processed/cleaned_materials.csv")
    
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        exit(1)
    
    df_cleaned = clean_dataset(input_path, output_path)
    
    # Display sample
    print("\nFirst 5 rows of cleaned data:")
    print(df_cleaned.head().to_string())
