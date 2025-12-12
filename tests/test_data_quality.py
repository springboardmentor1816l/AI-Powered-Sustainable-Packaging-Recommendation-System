
import pandas as pd
import numpy as np

DF_PATH = "/content/ecopackai/data/processed/cleaned_integrated_materials.csv"

def load_df():
    return pd.read_csv(DF_PATH)

def test_required_columns_present():
    df = load_df()
    required = ["Material ID","Material Type","Cost per Unit (USD)","CO2 Emission per kg (estimated)"] # Adjusted column names
    for c in required:
        assert c in df.columns, f"Missing required column: {c}"

def test_no_nan_in_mandatory():
    df = load_df()
    # Adjusted mandatory column names to match the DataFrame
    mandatory = ["Material ID", "Packaging Type", "Material Type", "Cost per Unit (USD)", "CO2 Emission per kg (estimated)"]
    for c in mandatory:
        assert df[c].isna().sum() == 0, f"NaNs in mandatory col: {c}"

def test_unique_materialid():
    df = load_df()
    assert df["Material ID"].is_unique, "Material ID not unique" # Adjusted column name

def test_no_duplicates_rows():
    df = load_df()
    assert df.duplicated().sum() == 0, "There are duplicate rows"

def test_value_ranges():
    df = load_df()
    # Adjusted column names to match the DataFrame
    if "Cost per Unit (USD)" in df.columns:
        assert (df["Cost per Unit (USD)"] > 0).all(), "Cost per Unit (USD) must be > 0"
    if "CO2 Emission per kg (estimated)" in df.columns:
        assert (df["CO2 Emission per kg (estimated)"] >= 0).all(), "CO2 Emission per kg (estimated) must be >= 0"
    if "Biodegradation Time (days)" in df.columns:
        assert (df["Biodegradation Time (days)"] >= 1).all(), "Biodeg days >= 1"
    # Adjusted column names to match the DataFrame
    for c in ["Moisture Resistance Score","Thermal Resistance Score"]:
        if c in df.columns:
            assert df[c].between(1,10).all(), f"{c} must be 1..10"

def test_categorical_values():
    df = load_df()
    # example checks:
    if "Recyclability Category" in df.columns:
        assert set(df["Recyclability Category"].dropna().unique()).issubset(set(["High","Medium","Unknown"])), "Invalid recyclability categories" # Adjusted expected categories

def test_feature_columns_range_if_present():
    df = load_df()
    for feat in ["CO2_Impact_Index","Cost_Efficiency_Index","Material_Suitability_Score"]:
        if feat in df.columns:
            assert df[feat].between(0,100).all(), f"{feat} must be 0..100"
