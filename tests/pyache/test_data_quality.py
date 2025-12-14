import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/engineered_features.csv")

# ---- Helper to safely check columns ----
def has_column(col):
    return col in df.columns

# ---------- STRUCTURE TESTS ----------

def test_required_columns_exist():
    required_columns = [
        "CII",
        "CEI",
        "MSS",
        "Final_Recommendation_Score"
    ]
    for col in required_columns:
        assert has_column(col), f"Missing column: {col}"

# ---------- MISSING VALUE TESTS ----------

def test_no_nulls_in_engineered_scores():
    score_cols = ["CII", "CEI", "MSS", "Final_Recommendation_Score"]
    for col in score_cols:
        assert df[col].isna().sum() == 0

# ---------- RANGE TESTS ----------

def test_scores_within_range():
    for col in ["CII", "CEI", "MSS", "Final_Recommendation_Score"]:
        assert df[col].between(0, 100).all()

# ---------- DATA TYPE TESTS ----------

def test_scores_are_numeric():
    for col in ["CII", "CEI", "MSS", "Final_Recommendation_Score"]:
        assert np.issubdtype(df[col].dtype, np.number)

# ---------- DUPLICATE CHECK ----------

def test_no_duplicate_rows():
    assert df.duplicated().sum() == 0

# ---------- INFINITE VALUES CHECK ----------

def test_no_infinite_values():
    assert np.isfinite(df.select_dtypes(include=[np.number])).all().all()
