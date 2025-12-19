import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import os

# Paths
X_PATH = "data/final/X_raw.csv"
OUT_PATH = "data/final/X_encoded_scaled.csv"
ENCODER_PATH = "models/encoders/ohe_encoder.pkl"
SCALER_PATH = "models/scalers/numeric_scaler.pkl"

os.makedirs("models/encoders", exist_ok=True)
os.makedirs("models/scalers", exist_ok=True)

# Load
X = pd.read_csv(X_PATH)

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

# Encode categoricals
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_cat = ohe.fit_transform(X[CATEGORICAL_FEATURES])
X_cat_df = pd.DataFrame(
    X_cat,
    columns=ohe.get_feature_names_out(CATEGORICAL_FEATURES)
)

# Scale numerics
scaler = StandardScaler()
X_num = scaler.fit_transform(X[NUMERIC_FEATURES])
X_num_df = pd.DataFrame(X_num, columns=NUMERIC_FEATURES)

# Combine
X_final = pd.concat([X_num_df, X_cat_df], axis=1)

# Save
X_final.to_csv(OUT_PATH, index=False)
joblib.dump(ohe, ENCODER_PATH)
joblib.dump(scaler, SCALER_PATH)

print("✅ Encoding & scaling completed")
print("Final shape:", X_final.shape)
