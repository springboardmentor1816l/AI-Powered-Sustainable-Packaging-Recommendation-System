import pandas as pd
import joblib
import numpy as np

# -----------------------------
# Paths
# -----------------------------
MODEL_PATH = "models/baseline/best_material_classifier.pkl"
ENCODER_PATH = "models/encoders/ohe_encoder.pkl"
SCALER_PATH = "models/scalers/numeric_scaler.pkl"
DATA_PATH = "data/final/materials_engineered.parquet"
OUT_PATH = "data/final/material_recommendations.csv"

# -----------------------------
# Load artifacts
# -----------------------------
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
scaler = joblib.load(SCALER_PATH)

df = pd.read_parquet(DATA_PATH)

# -----------------------------
# Feature definitions (MUST MATCH TRAINING)
# -----------------------------
CATEGORICAL_FEATURES = [
    "material_type",
    "Recyclability Category"
]

NUMERIC_FEATURES = [
    "moisture_resistance_score",
    "thermal_resistance_score",
    "Load Handling Score",
    "CO2 Emission per kg (estimated)",
    "Biodegradation Time (days)",
    "Reusability (%)",
    "supplier_sustainability_compliance_pct",
    "Waste Reduction Impact (%)",
    "Sustainability Target Progress (%)",
    "Cost per Unit (USD)",
    "Annual Usage (units)",
    "Total Material Weight (tons)",
    "CII",
    "CEI",
    "MSS"
]

# -----------------------------
# Apply SAME preprocessing
# -----------------------------
X_cat = encoder.transform(df[CATEGORICAL_FEATURES])
X_cat_df = pd.DataFrame(
    X_cat,
    columns=encoder.get_feature_names_out(CATEGORICAL_FEATURES)
)

X_num = scaler.transform(df[NUMERIC_FEATURES])
X_num_df = pd.DataFrame(X_num, columns=NUMERIC_FEATURES)

X_final = pd.concat([X_num_df, X_cat_df], axis=1)

# -----------------------------
# Predict probabilities
# -----------------------------
proba = model.predict_proba(X_final)
classes = model.classes_

proba_df = pd.DataFrame(proba, columns=classes)

# -----------------------------
# Normalize scores
# -----------------------------
df["MSS_norm"] = df["MSS"] / 100
df["CEI_norm"] = df["CEI"] / 100

# -----------------------------
# Ranking logic
# -----------------------------
recommendations = []

for idx, row in df.iterrows():
    for material in classes:
        score = (
            0.5 * proba_df.loc[idx, material]
            + 0.3 * row["MSS_norm"]
            + 0.2 * row["CEI_norm"]
        )

        recommendations.append({
            "row_id": idx,
            "material": material,
            "final_score": round(score, 4)
        })

rec_df = pd.DataFrame(recommendations)

top_k = (
    rec_df
    .sort_values(["row_id", "final_score"], ascending=[True, False])
    .groupby("row_id")
    .head(3)
)

# -----------------------------
# Save output
# -----------------------------
top_k.to_csv(OUT_PATH, index=False)

print("✅ Recommendation ranking completed")
print(f"📁 Output saved to: {OUT_PATH}")
