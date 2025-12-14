import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# ==============================
# Paths
# ==============================
INPUT_PATH = "data/processed/cleaned_dataset.csv"
OUTPUT_PATH = "data/model_ready/materials_encoded_scaled.csv"

ENCODER_PATH = "models/encoders/categorical_encoder.pkl"
SCALER_PATH = "models/scalers/numeric_scaler.pkl"

# ==============================
# Load dataset
# ==============================
print("📥 Loading cleaned dataset...")
df = pd.read_csv(INPUT_PATH)

# ==============================
# Drop non-ML columns
# ==============================
if "Material ID" in df.columns:
    df = df.drop(columns=["Material ID"])

# ==============================
# Define columns
# ==============================
categorical_cols = [
    "Packaging Type",
    "Material Type",
    "Suitable Product Categories",
    "Recommended Packaging Use Cases",
    "Supplier Region",
    "Recyclability Category"
]

numeric_cols = [
    "Recyclability (%)",
    "Recycled Content (%)",
    "Reusability (%)",
    "Biodegradation Time (days)",
    "End-of-Life Disposal (%)",
    "Carbon Footprint (kg CO2/unit)",
    "CO2 Emission per kg (estimated)",
    "Waste Reduction Impact (%)",
    "Sustainability Target Progress (%)",
    "Load Handling Score",
    "Moisture Resistance Score",
    "Thermal Resistance Score",
    "Cost per Unit (USD)",
    "Annual Usage (units)",
    "Total Material Weight (tons)",
    "Supplier Sustainability Compliance (%)"
]

# ==============================
# Encode categorical features
# ==============================
print("🔠 Encoding categorical features...")
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_array = ohe.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(
    encoded_array,
    columns=ohe.get_feature_names_out(categorical_cols)
)

# Save encoder
joblib.dump(ohe, ENCODER_PATH)

# ==============================
# Scale numeric features
# ==============================
print("📏 Scaling numeric features...")
scaler = MinMaxScaler()
scaled_array = scaler.fit_transform(df[numeric_cols])
scaled_df = pd.DataFrame(scaled_array, columns=numeric_cols)

# Save scaler
joblib.dump(scaler, SCALER_PATH)

# ==============================
# Combine final dataset
# ==============================
final_df = pd.concat([scaled_df, encoded_df], axis=1)

# ==============================
# Save output
# ==============================
final_df.to_csv(OUTPUT_PATH, index=False)

print("✅ Day 9 completed successfully!")
print(f"📁 Output saved to: {OUTPUT_PATH}")
