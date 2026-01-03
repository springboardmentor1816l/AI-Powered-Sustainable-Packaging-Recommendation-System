# EcoPackAI/src/inference/predictor.py

import joblib
import pandas as pd
from pathlib import Path
from pandas.api.types import is_object_dtype

# =====================
# PATHS (ROOT SAFE)
# =====================
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "ml/models/xgb_co2.joblib"

# =====================
# LOAD MODEL
# =====================
print("⚙️ Loading model for inference...")
model = joblib.load(MODEL_PATH)

FEATURES = list(model.feature_names_in_)
print(f"✅ Model expects {len(FEATURES)} features")

# =====================
# PREDICT FUNCTION
# =====================
def predict(input_df: pd.DataFrame) -> pd.Series:
    """
    Batch or single-row prediction.
    """
    X = input_df.copy()

    # Enforce training feature set
    X = X[FEATURES]

    # Encode categoricals
    for col in X.columns:
        if is_object_dtype(X[col]):
            X[col] = X[col].astype("category").cat.codes

    X = X.astype(float)

    preds = model.predict(X)
    return pd.Series(preds, index=X.index)
