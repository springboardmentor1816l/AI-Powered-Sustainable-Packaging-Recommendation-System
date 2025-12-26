import json
import pandas as pd

def preprocess_industry(df, reference_columns=None):
    # Load fixed leakage rules (industry standard)
    with open("ml/leakage_columns.json", "r") as f:
        leakage_cols = json.load(f)

    # 1. Remove leakage columns
    df = df.drop(columns=[c for c in leakage_cols if c in df.columns])

    # 2. Encode categorical features
    df = pd.get_dummies(df, drop_first=True)

    # 3. Align columns (for inference)
    if reference_columns is not None:
        df = df.reindex(columns=reference_columns, fill_value=0)

    return df
