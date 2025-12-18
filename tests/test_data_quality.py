import pandas as pd
import numpy as np

DATA_PATH = "data/interim/materials_cleaned.csv"

MANDATORY_COLS = [
    "Cost per Unit (USD)",
    "CO2 Emission per kg (estimated)",
    "Biodegradation Time (days)",
    "moisture_resistance_score",
    "thermal_resistance_score"
]

PERCENTAGE_COLS = [
    "Reusability (%)",
    "End-of-Life Disposal (%)",
    "Waste Reduction Impact (%)",
    "Sustainability Target Progress (%)",
    "supplier_sustainability_compliance_pct"
]


def load_data():
    return pd.read_csv(DATA_PATH)


# -----------------------
# STRUCTURAL TESTS
# -----------------------

def test_dataset_not_empty():
    df = load_data()
    assert df.shape[0] > 0, "Dataset is empty"


def test_no_duplicate_rows():
    df = load_data()
    assert df.duplicated().sum() == 0, "Duplicate rows found"


def test_required_columns_exist():
    df = load_data()
    for col in MANDATORY_COLS:
        assert col in df.columns, f"Missing required column: {col}"


# -----------------------
# NULL CHECKS
# -----------------------

def test_no_nulls_in_mandatory_columns():
    df = load_data()
    for col in MANDATORY_COLS:
        assert df[col].isnull().sum() == 0, f"Nulls found in {col}"


# -----------------------
# NUMERIC RANGE TESTS
# -----------------------

def test_cost_positive():
    df = load_data()
    assert (df["Cost per Unit (USD)"] > 0).all()


def test_co2_non_negative():
    df = load_data()
    assert (df["CO2 Emission per kg (estimated)"] >= 0).all()


def test_biodegradation_valid():
    df = load_data()
    assert (df["Biodegradation Time (days)"] >= 1).all()


def test_resistance_scores_range():
    df = load_data()
    assert df["moisture_resistance_score"].between(1, 10).all()
    assert df["thermal_resistance_score"].between(1, 10).all()


def test_percentage_columns_range():
    df = load_data()
    for col in PERCENTAGE_COLS:
        if col in df.columns:
            assert df[col].between(0, 100).all(), f"{col} out of range"


# -----------------------
# INVALID VALUE TESTS
# -----------------------

def test_no_infinite_values():
    df = load_data()
    assert np.isinf(df.select_dtypes(include=[np.number])).sum().sum() == 0
