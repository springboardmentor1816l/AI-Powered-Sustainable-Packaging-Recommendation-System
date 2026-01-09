import pandas as pd
import numpy as np

DATA_PATH = "data/final/materials_final_encoded.csv"
df = pd.read_csv(DATA_PATH)


def test_dataset_not_empty():
    assert df.shape[0] > 0


def test_no_duplicate_rows():
    assert df.duplicated().sum() == 0


def test_expected_numeric_columns_exist():
    expected_numeric = [
        "cost_per_kg",
        "recyclability_percent",
        "strength_mpa",
        "co2_emission_score"
    ]
    for col in expected_numeric:
        assert col in df.columns


def test_one_hot_encoded_columns_exist():
    encoded_cols = [c for c in df.columns if "material_type_" in c]
    assert len(encoded_cols) > 0


def test_scaled_numeric_ranges():
    numeric_df = df.select_dtypes(include=[np.number])
    assert (numeric_df >= 0).all().all()
    assert (numeric_df <= 1).all().all()


def test_no_null_values():
    assert df.isnull().sum().sum() == 0


def test_no_infinite_values():
    numeric_df = df.select_dtypes(include=[np.number])
    assert np.isfinite(numeric_df.values).all()
