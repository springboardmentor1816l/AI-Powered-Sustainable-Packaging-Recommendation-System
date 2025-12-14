import pandas as pd
import pytest
from pathlib import Path

DATA_PATH = Path("../data/model_ready/materials_final_encoded.csv")

@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)

# --------------------------------------------------
# Structural Tests
# --------------------------------------------------

def test_required_columns_exist(df):
    required_columns = [
        "Material ID",
        "Packaging Type",
        "Material Type",
        "Supplier Region",
        "Recyclability (%)",
        "Recycled Content (%)",
        "Reusability (%)",
        "Biodegradation Time (days)",
        "End-of-Life Disposal (%)",
        "Carbon Footprint (kg CO2/unit)",
        "CO2 Emission per kg (estimated)",
        "Waste Reduction Impact (%)",
        "Sustainability Target Progress (%)",
        "Load Handling Score",
        "Moisture Resistance Score",
        "Thermal Resistance Score",
        "Cost per Unit (USD)",
        "Annual Usage (units)",
        "Total Material Weight (tons)",
        "Supplier Sustainability Compliance (%)"
    ]

    for col in required_columns:
        assert col in df.columns, f"Missing required column: {col}"

# --------------------------------------------------
# Missing Value Tests
# --------------------------------------------------

def test_no_missing_values(df):
    assert df.isnull().sum().sum() == 0, "Dataset contains missing values"

# --------------------------------------------------
# Range Tests
# --------------------------------------------------

def test_percentage_ranges(df):
    percentage_cols = [c for c in df.columns if "%" in c]
    for col in percentage_cols:
        assert df[col].between(0, 100).all(), f"Invalid percentage range in {col}"

def test_non_negative_numeric_columns(df):
    # Columns that must always be non-negative (business constraints)
    non_negative_cols = [
        "Recyclability (%)",
        "Recycled Content (%)",
        "Reusability (%)",
        "End-of-Life Disposal (%)",
        "Waste Reduction Impact (%)",
        "Sustainability Target Progress (%)",
        "Load Handling Score",
        "Moisture Resistance Score",
        "Thermal Resistance Score",
        "Cost per Unit (USD)",
        "Annual Usage (units)",
        "Total Material Weight (tons)",
        "Supplier Sustainability Compliance (%)",
        "CO2 Emission per kg (estimated)"
    ]

    for col in non_negative_cols:
        assert (df[col] >= 0).all(), f"Negative values found in {col}"

def test_standard_scaled_columns_can_be_negative(df):
    standard_scaled_cols = [
        "Biodegradation Time (days)",
        "Carbon Footprint (kg CO2/unit)"
    ]

    for col in standard_scaled_cols:
        assert df[col].dtype != object

def test_cost_positive(df):
    assert (df["Cost per Unit (USD)"] > 0).all(), "Cost per Unit must be > 0"

# --------------------------------------------------
# Encoded Feature Tests
# --------------------------------------------------

def test_onehot_columns_binary(df):
    encoded_cols = [c for c in df.columns if "product_cat_" in c or "usecase_" in c]
    for col in encoded_cols:
        assert set(df[col].unique()).issubset({0, 1}), f"Non-binary values in {col}"

# --------------------------------------------------
# Integrity Tests
# --------------------------------------------------

def test_material_id_unique(df):
    assert df["Material ID"].is_unique, "Material ID values are not unique"

def test_no_duplicate_rows(df):
    assert not df.duplicated().any(), "Duplicate rows found in dataset"
