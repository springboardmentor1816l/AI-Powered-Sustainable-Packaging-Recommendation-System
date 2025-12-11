import pandas as pd
import pytest

# Load the processed dataset
materials = pd.read_csv("data/processed/materials_final_scores.csv")

# ------------------- Test Cases -------------------

def test_required_columns():
    required = [
        "material_id",
        "material_type",
        "cost_per_kg",
        "co2_emission_kg_per_kg",
        "recyclability_category",
        "co2_impact_index",
        "cost_efficiency_index",
        "material_suitability_score"
    ]
    for col in required:
        assert col in materials.columns, f"Missing column: {col}"

def test_no_null_values():
    required_cols = [
        "material_type", "cost_per_kg", "co2_emission_kg_per_kg",
        "recyclability_category", "co2_impact_index",
        "cost_efficiency_index", "material_suitability_score"
    ]
    for col in required_cols:
        assert materials[col].isna().sum() == 0, f"Null values found in {col}"

def test_valid_recyclability_category():
    valid_categories = {"A", "B", "C", "D"}
    unique_vals = set(materials["recyclability_category"].unique())
    assert unique_vals.issubset(valid_categories), "Invalid recyclability category detected"

def test_positive_values():
    assert (materials["cost_per_kg"] > 0).all(), "Cost contains non-positive values"
    assert (materials["co2_emission_kg_per_kg"] >= 0).all(), "Negative CO₂ emission found"

def test_score_ranges():
    assert (materials["co2_impact_index"].between(0, 100)).all(), "CO₂ impact score out of range"
    assert (materials["cost_efficiency_index"].between(0, 100)).all(), "Cost efficiency score out of range"
    assert (materials["material_suitability_score"].between(0, 100)).all(), "Material suitability score out of range"

def test_material_id_uniqueness():
    assert materials["material_id"].is_unique, "Duplicate material_id found"
