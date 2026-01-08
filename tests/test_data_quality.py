import pandas as pd

def load_data():
    return pd.read_csv("data/processed/materials.csv")

def test_required_columns_present():
    df = load_data()
    required_columns = ["Material", "Cost/kg", "CO2_emission"]
    for col in required_columns:
        assert col in df.columns

def test_no_nulls_in_mandatory_columns():
    df = load_data()
    assert df["Material"].isnull().sum() == 0
    assert df["Cost/kg"].isnull().sum() == 0
    assert df["CO2_emission"].isnull().sum() == 0

def test_cost_positive():
    df = load_data()
    assert (df["Cost/kg"] > 0).all()

def test_no_duplicate_rows():
    df = load_data()
    assert df.duplicated().sum() == 0
