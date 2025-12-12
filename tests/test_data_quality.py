import pandas as pd
import pytest

# Load dataset
@pytest.fixture
def df():
    return pd.read_csv('data/model_ready/materials_final_encoded.csv')

# -----------------------------
# 1. Structural Tests
# -----------------------------

def test_required_columns_exist(df):
    required_cols = [
        'Material ID','Recyclability (%)','Recycled Content (%)','Reusability (%)',
        'Biodegradation Time (days)','End-of-Life Disposal (%)','Carbon Footprint (kg CO2/unit)',
        'CO2 Emission per kg (estimated)','Waste Reduction Impact (%)','Sustainability Target Progress (%)',
        'Load Handling Score','Moisture Resistance Score','Thermal Resistance Score','Cost per Unit (USD)',
        'Annual Usage (units)','Total Material Weight (tons)','Supplier Sustainability Compliance (%)'
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"


def test_no_extra_columns(df):
    # User can update if new columns added intentionally
    assert len(df.columns) >= 47, "Unexpected missing columns detected"

# -----------------------------
# 2. Cleanliness Tests
# -----------------------------

def test_no_nulls_in_required_columns(df):
    required_cols = [
        'Material ID','Recyclability (%)','Recycled Content (%)','Reusability (%)',
        'Biodegradation Time (days)','End-of-Life Disposal (%)','Carbon Footprint (kg CO2/unit)',
        'CO2 Emission per kg (estimated)','Waste Reduction Impact (%)','Sustainability Target Progress (%)',
        'Load Handling Score','Moisture Resistance Score','Thermal Resistance Score','Cost per Unit (USD)',
        'Annual Usage (units)','Total Material Weight (tons)','Supplier Sustainability Compliance (%)'
    ]
    assert df[required_cols].isnull().sum().sum() == 0, "Nulls found in mandatory fields"


def test_unique_material_id(df):
    assert df['Material ID'].is_unique, "Duplicate Material ID detected"


# -----------------------------
# 3. Range Tests
# -----------------------------

def test_non_negative_numeric_values(df):
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    assert (df[numeric_cols] >= 0).all().all(), "Negative values found in numeric columns"


def test_score_ranges(df):
    for col in ['Load Handling Score','Moisture Resistance Score','Thermal Resistance Score']:
        assert df[col].between(0,1).all(), f"{col} contains values outside 0–1 range"


# -----------------------------
# 4. One-Hot Encoding Tests
# -----------------------------

def test_one_hot_values(df):
    one_hot_cols = [
        col for col in df.columns if 'Packaging Type_' in col
        or 'Material Type_' in col
        or 'Recyclability Category_' in col
        or 'Supplier Region_' in col
        or 'Suitable Product Categories_' in col
        or 'Recommended Packaging Use Cases_' in col
    ]
    assert df[one_hot_cols].isin([0,1]).all().all(), "One-hot columns must contain only 0 or 1"


def test_material_type_one_hot(df):
    cols = ['Material Type_Cardboard','Material Type_Paper/Bio-Based','Material Type_Plastic','Material Type_Steel']
    assert (df[cols].sum(axis=1) == 1).all(), "Exactly one Material Type must be 1"


def test_recyclability_category_one_hot(df):
    cols = ['Recyclability Category_High','Recyclability Category_Medium']
    assert (df[cols].sum(axis=1) == 1).all(), "Exactly one recyclability category must be 1"


def test_supplier_region_one_hot(df):
    cols = ['Supplier Region_AMERICAS','Supplier Region_APAC','Supplier Region_EMEA','Supplier Region_EU','Supplier Region_LATAM','Supplier Region_ROW']
    assert (df[cols].sum(axis=1) == 1).all(), "Exactly one supplier region must be 1"

# -----------------------------
# 5. Feature Engineering (If Added)
# -----------------------------

def test_engineered_scores_valid(df):
    engineered_cols = [col for col in df.columns if col in ['cii','cei','mss','recommendation_score']]
    if engineered_cols:
        for col in engineered_cols:
            assert df[col].between(0,100).all(), f"Feature {col} must be between 0 and 100"
            assert df[col].notnull().all(), f"Feature {col} contains null values"