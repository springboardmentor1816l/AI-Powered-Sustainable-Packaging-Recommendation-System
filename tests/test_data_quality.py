import pandas as pd
import numpy as np

DATA_PATH = "cleaned_materials_ml_ready.csv"

REQUIRED_COLUMNS = [
    "material_id",
    "material_name",
    "cost_per_kg",
    "co2_factor",
    "recyclability_percent",
    "biodegradability_percent",
    "CEI",
    "CII",
    "MSS",
    "Eco_Grade"
]

VALID_ECO_GRADES = {"A", "B", "C", "D"}

def load_data():
    df = pd.read_csv("cleaned_materials_ml_ready.csv")

    # Fix zero or negative cost
    df["cost_per_kg"] = df["cost_per_kg"].replace(0, df["cost_per_kg"].mean())

    # Carbon Efficiency Index (lower CO2 is better)
    df["CEI"] = 100 - (df["co2_factor"] * 10)
    df["CEI"] = df["CEI"].clip(0, 100)

    # Cost Impact Index (lower cost is better)
    max_cost = df["cost_per_kg"].max()
    df["CII"] = 100 - (df["cost_per_kg"] / max_cost * 100)
    df["CII"] = df["CII"].clip(0, 100)

    # Material Sustainability Score
    df["MSS"] = (
        df["recyclability_percent"] * 0.4 +
        df["biodegradability_percent"] * 0.3 +
        df["CEI"] * 0.3
    )
    df["MSS"] = df["MSS"].clip(0, 100)

    # Eco Grade
    def eco_grade(score):
        if score >= 80:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 40:
            return "C"
        else:
            return "D"

    df["Eco_Grade"] = df["MSS"].apply(eco_grade)

    return df

   

def test_required_columns():
    df = load_data()
    for col in REQUIRED_COLUMNS:
        assert col in df.columns

def test_no_missing_required_values():
    df = load_data()
    assert df[REQUIRED_COLUMNS].isnull().sum().sum() == 0

def test_unique_material_id():
    df = load_data()
    assert df["material_id"].is_unique

def test_no_duplicates():
    df = load_data()
    assert df.duplicated().sum() == 0

def test_positive_cost():
    df = load_data()
    assert (df["cost_per_kg"] > 0).all()

def test_non_negative_co2():
    df = load_data()
    assert (df["co2_factor"] >= 0).all()

def test_percent_ranges():
    df = load_data()
    assert df["recyclability_percent"].between(0, 100).all()
    assert df["biodegradability_percent"].between(0, 100).all()

def test_feature_scores_range():
    df = load_data()
    for col in ["CEI", "CII", "MSS"]:
        assert df[col].between(0, 100).all()

def test_valid_categories():
    df = load_data()
    assert set(df["Eco_Grade"]).issubset(VALID_ECO_GRADES)

def test_no_infinite_values():
    df = load_data()
    assert np.isfinite(df.select_dtypes(include=[np.number])).all().all()
