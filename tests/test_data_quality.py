
import pandas as pd
import numpy as np
from pytest import fixture
import pytest

# --- FILE PATHS (Adjust this path to where your final data is located) ---
DATA_PATH = 'materials_final_engineered.csv' 

# --- COLUMN DEFINITIONS (Must match the engineered data) ---
COLS_MANDATORY_NOT_NULL = ['Material ID', 'Cost per Unit (USD)', 'CO2 Emission per kg (estimated)']
COLS_NON_NEGATIVE = ['Cost per Unit (USD)', 'CO2 Emission per kg (estimated)', 'Biodegradation Time (days)']
COLS_ENGINEERED = ['CO2_Impact_Index', 'Cost_Efficiency_Index', 'Material_Suitability_Score']
OHE_CATEGORY_PREFIXES = ['Packaging Type_', 'Material Type_', 'Recyclability Category_']

@pytest.fixture(scope="session")
def final_engineered_data():
    """Fixture to load the final engineered dataset once per session."""
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        pytest.skip(f"Skipping data quality tests because input file {DATA_PATH} was not found.")

class TestDataQuality:
    
    # --- Structural Tests ---
    def test_01_mandatory_columns_exist(self, final_engineered_data):
        """Asserts that all mandatory columns are present (Structural Test)."""
        df = final_engineered_data
        missing_cols = [col for col in COLS_MANDATORY_NOT_NULL if col not in df.columns]
        assert not missing_cols, f"Mandatory columns missing: {missing_cols}"
        
    def test_02_material_id_is_unique(self, final_engineered_data):
        """Asserts that Material ID is unique (Uniqueness Test)."""
        df = final_engineered_data
        assert df['Material ID'].nunique() == len(df), "Material ID column contains non-unique values."
        
    def test_03_no_duplicate_rows(self, final_engineered_data):
        """Asserts that there are no duplicate rows (Integrity Test)."""
        df = final_engineered_data
        assert df.duplicated().sum() == 0, f"Found {df.duplicated().sum()} duplicate rows."

    # --- Cleanliness & Range Tests ---
    def test_04_no_nulls_in_mandatory_fields(self, final_engineered_data):
        """Asserts that mandatory fields (Cost, CO2) are non-null (Cleanliness Test)."""
        df = final_engineered_data
        null_counts = df[COLS_MANDATORY_NOT_NULL].isnull().sum()
        assert null_counts.sum() == 0, f"Nulls found in mandatory columns: {null_counts[null_counts > 0].to_dict()}"

    def test_05_no_infinity_or_invalid_values(self, final_engineered_data):
        """Asserts that no feature produces infinity or invalid values (Feature Engineering Test)."""
        df = final_engineered_data
        is_inf = np.isinf(df.select_dtypes(include=np.number)).sum().sum()
        assert is_inf == 0, f"Found {is_inf} infinity values. Check engineering formulas."

    def test_06_non_negative_values(self, final_engineered_data):
        """Asserts that core values expected to be non-negative are >= 0 (Range Test)."""
        df = final_engineered_data
        non_negative_violations = df[COLS_NON_NEGATIVE].lt(0).sum().sum()
        assert non_negative_violations == 0, f"Found {non_negative_violations} values < 0 in non-negative columns."

    # --- Scaling & Feature Engineering Tests ---
    def test_07_scaling_range_is_0_to_1(self, final_engineered_data):
        """Asserts that all numeric features are scaled within the [0.0, 1.0] range (Range/Scaling Test)."""
        df = final_engineered_data
        numeric_df = df.select_dtypes(include=np.number).drop(columns=['Material ID'], errors='ignore')
        
        # Check against a small tolerance for floating point errors
        max_violation = numeric_df.gt(1.0 + 1e-6).sum().sum()
        min_violation = numeric_df.lt(0.0 - 1e-6).sum().sum()
        
        assert max_violation == 0 and min_violation == 0,             f"Scaling range violation: {max_violation} values > 1.0, {min_violation} values < 0.0"

    def test_08_ohe_features_are_binary(self, final_engineered_data):
        """Asserts that all OHE features contain only 0 or 1 (Categorical Test)."""
        df = final_engineered_data
        
        # Identify OHE columns dynamically using prefixes
        ohe_cols = [col for col in df.columns if any(col.startswith(p) for p in OHE_CATEGORY_PREFIXES)]
        
        if ohe_cols:
            ohe_df = df[ohe_cols].copy()
            unique_values = np.unique(ohe_df.values)
            
            # Check if all unique values are close to 0 or 1
            is_binary = np.all(np.isclose(unique_values, 0.0) | np.isclose(unique_values, 1.0))
            
            assert is_binary, f"OHE columns contain non-binary values. Found unique values close to: {unique_values}"
        else:
            pytest.skip("No OHE columns found to test.")
