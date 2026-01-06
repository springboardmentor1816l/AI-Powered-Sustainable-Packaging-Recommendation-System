import pandas as pd
from sklearn.preprocessing import LabelEncoder

CATEGORICAL_COLS = [
    "category",
    "shipping_type",
    "material_type",
    "packaging_type",
    "supplier_region"
]

def preprocess_input(payload: dict) -> pd.DataFrame:
    df = pd.DataFrame([payload])

    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    return df
