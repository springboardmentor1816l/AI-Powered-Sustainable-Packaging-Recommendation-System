import pandas as pd
import numpy as np

# load once (pytest will import this module)
DF_PATH = "data/processed/cleaned_dataset.csv"
df = pd.read_csv(DF_PATH)

# Helper: list of columns (as given)
REQUIRED_COLUMNS = [
    "Material ID",
    "Packaging Type",
    "Material Type",
    "Suitable Product Categories",
    "Recommended Packaging Use Cases",
    "Supplier Region",
    "Recyclability (%)",
    "Recyclability Category",
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

# ---- Structural tests ----
def test_all_columns_present():
    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing column: {col}"

def test_no_duplicate_column_names():
    assert len(df.columns) == len(set(df.columns)), "Duplicate column names found"

# ---- Cleanliness / mandatory non-null tests ----
MANDATORY_NON_NULL = [
    "Material ID",
    "Material Type",
    "Cost per Unit (USD)",
    "CO2 Emission per kg (estimated)",
    "Biodegradation Time (days)"
]

def test_mandatory_columns_not_null():
    for col in MANDATORY_NON_NULL:
        nulls = df[col].isnull().sum()
        assert nulls == 0, f"Mandatory column {col} has {nulls} null(s)"

def test_no_duplicate_rows():
    dup_count = df.duplicated().sum()
    assert dup_count == 0, f"Found {dup_count} duplicate rows"

# ---- Ranges / numeric validity tests ----
def _assert_between(series, low, high, colname):
    # ignore nulls for optional columns
    s = series.dropna()
    if s.empty:
        return
    assert s.ge(low).all() and s.le(high).all(), f"Column {colname} out of range [{low},{high}]"

def test_cost_positive():
    assert (df["Cost per Unit (USD)"].dropna() > 0).all(), "Cost per Unit must be > 0"

def test_co2_non_negative():
    assert (df["CO2 Emission per kg (estimated)"].dropna() >= 0).all(), "CO2 per kg must be >= 0"
    assert (df["Carbon Footprint (kg CO2/unit)"].dropna() >= 0).all(), "Carbon Footprint must be >= 0"

def test_biodegradation_min_1():
    assert (df["Biodegradation Time (days)"].dropna() >= 1).all(), "Biodegradation Time must be >= 1"

def test_percent_columns_range():
    percent_cols = [
        "Recyclability (%)",
        "Recycled Content (%)",
        "Reusability (%)",
        "End-of-Life Disposal (%)",
        "Waste Reduction Impact (%)",
        "Sustainability Target Progress (%)",
        "Supplier Sustainability Compliance (%)"
    ]
    for col in percent_cols:
        _assert_between(df[col], 0, 100, col)

def test_scores_range_1_10():
    score_cols = ["Load Handling Score", "Moisture Resistance Score", "Thermal Resistance Score"]
    for col in score_cols:
        _assert_between(df[col], 1, 10, col)

def test_usage_and_weight_non_negative():
    assert (df["Annual Usage (units)"].dropna() >= 0).all(), "Annual Usage must be >= 0"
    assert (df["Total Material Weight (tons)"].dropna() >= 0).all(), "Total Material Weight must be >= 0"

# ---- Categorical validity ----
def test_material_type_allowed_values():
    allowed = {
        "Paper", "Plastic", "Metal", "Bio-based",
        "Steel", "Cardboard", "Paper/Bio-Based"
    }

    # Only check non-null values
    vals = set(df["Material Type"].dropna().unique())
    bad = vals - allowed
    assert not bad, f"Unexpected Material Type values found: {bad}"

def test_recyclability_category_allowed():
    allowed = {"A", "B", "C", "D", "High", "Medium", "Low"}

    vals = set(df["Recyclability Category"].dropna().astype(str).unique())
    bad = vals - allowed
    assert not bad, f"Unexpected Recyclability Category values found: {bad}"

# ---- Uniqueness ----
def test_material_id_unique():
    dup = df["Material ID"].duplicated().sum()
    assert dup == 0, f"Material ID not unique: {dup} duplicates"
