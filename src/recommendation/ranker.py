import joblib
import pandas as pd

MODEL_PATH = "ml/models/rf_cost_pipeline.joblib"
model = joblib.load(MODEL_PATH)

# These are the raw features the model expects
EXPECTED = list(model.feature_names_in_)

def rank_materials(df):

    df = df.copy()

    # Apply constraints on RAW data
    df = df[df["recyclability_percent"] >= 0.4]
    df = df[df["product_weight"] > 0]

    if df.empty:
        raise ValueError("No materials satisfy the constraints.")

    # Guarantee correct raw feature set
    for col in EXPECTED:
        if col not in df.columns:
            df[col] = 0

    df = df[EXPECTED]

    # 🔥 NO external pipeline — model already contains it
    df["predicted_cost"] = model.predict(df)

    # Final ranking
    # Fallback if CO2 column not present
    if "co2_emission_score" not in df.columns:
        df["co2_emission_score"] = 0.5  # neutral default

    df["final_score"] = (
        0.5 * (1 - df["predicted_cost"]) +
        0.3 * (1 - df["co2_emission_score"]) +
        0.2 * df["MSS"]
    )

    df = df.sort_values("final_score", ascending=False)
    df["rank"] = range(1, len(df) + 1)

    return df






