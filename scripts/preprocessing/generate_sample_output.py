import pandas as pd
import joblib
from pathlib import Path

X = pd.read_csv("../../data/model_input/X_raw.csv")
pipeline = joblib.load("../../models/preprocessing/preprocessing_pipeline.pkl")

X_transformed = pipeline.transform(X)

out = Path("../../data/model_ready")
out.mkdir(parents=True, exist_ok=True)

pd.DataFrame(X_transformed).head(50).to_csv(
    out / "sample_transformed.csv",
    index=False
)

print("Sample transformed output saved")
