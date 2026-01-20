import pandas as pd
import numpy as np
import os

# -------------------------------------------------
# Load dataset safely (path independent)
# -------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "cleaned_integrated_materials.csv"
)

def load_df():
    return pd.read_csv(DF_PATH)

# -------------------------------------------------
# 1. STRUCTURAL TESTS
# -------------------------------------------------

def test_required_columns_present():
    df = load_df()
    required_columns = [
        "Material ID",
        "Packaging Type",
        "Material Type",
        "Recyclability Category",
        "Cost per Unit (USD)",
        "CO2 Emission per kg (estimated)"
    ]
    for col in required_columns:
        assert col in df.columns, f"Missing required column: {col}"

def test_dataset_not_empty():
    df = load_df()
    assert len(df) > 0, "Dataset is empty"

# -------------------------------------------------
# 2. CLEANLINESS TESTS
# -------------------------------------------------

def test_no_nan_in_mandatory_columns():
    df = load_df()
    mandatory_columns = [
        "Material ID",
        "Packaging Type",
        "Material Type",
        "Cost per Unit (USD)",
        "CO2 Emission per kg (estimated)"
    ]
    for col in mandatory_columns:
        assert df[col].isna().sum() == 0, f"NaNs found in mandatory column: {col}"

def test_material_id_unique():
    df = load_df()
    assert df["Material ID"].is_unique, "Material ID values are not unique"

def test_no_duplicate_rows():
    df = load_df()
    assert df.duplicated().sum() == 0, "Duplicate rows found in dataset"

# -------------------------------------------------
# 3. RANGE TESTS
# -------------------------------------------------

def test_numeric_value_ranges():
    df = load_df()

    assert (df["Cost per Unit (USD)"] > 0).all(), "Cost per Unit must be > 0"
    assert (df["CO2 Emission per kg (estimated)"] >= 0).all(), "CO2 emission must be >= 0"

    if "Biodegradation Time (days)" in df.columns:
        assert (df["Biodegradation Time (days)"] >= 1).all(), "Biodegradation days must be >= 1"

    for col in ["Moisture Resistance Score", "Thermal Resistance Score"]:
        if col in df.columns:
            assert df[col].between(1, 10).all(), f"{col} must be between 1 and 10"

# -------------------------------------------------
# 4. CATEGORICAL TESTS
# -------------------------------------------------

def test_valid_categorical_values():
    df = load_df()

    valid_packaging = {"Box", "Pouch", "Tray", "Wrap", "Compostable Sheet"}
    valid_materials = {"Paper", "Plastic", "Metal", "Bio-based"}
    valid_recyclability = {"A", "B", "C", "D"}

    if "Packaging Type" in df.columns:
        assert set(df["Packaging Type"].dropna().unique()).issubset(valid_packaging), \
            "Invalid Packaging Type values found"

    if "Material Type" in df.columns:
        assert set(df["Material Type"].dropna().unique()).issubset(valid_materials), \
            "Invalid Material Type values found"

    if "Recyclability Category" in df.columns:
        assert set(df["Recyclability Category"].dropna().unique()).issubset(valid_recyclability), \
            "Invalid Recyclability Category values found"

# -------------------------------------------------
# 5. ENGINEERED DATA SAFETY TESTS
# -------------------------------------------------

def test_feature_columns_range_if_present():
    df = load_df()
    for feat in [
        "CO2_Impact_Index",
        "Cost_Efficiency_Index",
        "Material_Suitability_Score"
    ]:
        if feat in df.columns:
            assert df[feat].between(0, 100).all(), f"{feat} must be between 0 and 100"

def test_no_infinite_or_invalid_numeric_values():
    df = load_df()
    numeric_df = df.select_dtypes(include=[np.number])
    assert np.isfinite(numeric_df).all().all(), "Infinite or invalid numeric values detected"
