import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import joblib
import os

INPUT_PATH = "data/processed/cleaned_dataset.csv"
OUTPUT_PATH = "data/model_ready/final_encoded_dataset.csv"
ENCODER_DIR = "models/encoders"
SCALER_DIR = "models/scalers"
REPORT_PATH = "docs/encoding_normalization_report.md"

os.makedirs("data/model_ready", exist_ok=True)
os.makedirs(ENCODER_DIR, exist_ok=True)
os.makedirs(SCALER_DIR, exist_ok=True)

print("📥 Loading cleaned dataset...")
df = pd.read_csv(INPUT_PATH)

# ---------------------------------
# 1️⃣ Identify Column Types
# ---------------------------------
numeric_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = df.select_dtypes(exclude=[np.number]).columns

print("\nNumeric Columns:", list(numeric_cols))
print("Categorical Columns:", list(categorical_cols))

# ---------------------------------
# 2️⃣ Encoding Categorical Columns
# ---------------------------------
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

encoded = ohe.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(encoded, columns=ohe.get_feature_names_out(categorical_cols))

# Save Encoder
joblib.dump(ohe, f"{ENCODER_DIR}/ohe_encoder.pkl")

# ---------------------------------
# 3️⃣ Normalize Numeric Values
# ---------------------------------
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[numeric_cols])
scaled_df = pd.DataFrame(scaled, columns=numeric_cols)

# Save Scaler
joblib.dump(scaler, f"{SCALER_DIR}/numeric_scaler.pkl")

# ---------------------------------
# 4️⃣ Combine Final ML Dataset
# ---------------------------------
final_df = pd.concat([scaled_df, encoded_df], axis=1)
final_df.to_csv(OUTPUT_PATH, index=False)

print(f"\n📤 Final encoded dataset saved to: {OUTPUT_PATH}")

# ---------------------------------
# 5️⃣ Write Report
# ---------------------------------
with open(REPORT_PATH, "w") as f:
    f.write("# Encoding & Normalization Report\n\n")
    f.write("## Categorical Columns Encoded\n")
    for col in categorical_cols:
        f.write(f"- {col}\n")

    f.write("\n## Numeric Columns Scaled (0-1)\n")
    for col in numeric_cols:
        f.write(f"- {col}\n")

print("\n✔ Encoding + normalization complete!")
