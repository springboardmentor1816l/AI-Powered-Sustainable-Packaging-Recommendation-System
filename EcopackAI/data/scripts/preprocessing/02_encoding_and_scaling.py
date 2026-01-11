import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# ------------------ PATHS ------------------
IN_PATH = Path("EcopackAI/data/processed/cleaned_integrated_materials.csv")
OUT_ENCODED_PATH = Path("EcopackAI/data/model_ready/materials_final_encoded.csv")

ENCODER_PATH = Path("EcopackAI/models/encoders/ohe_encoder.pkl")
SCALER_PATH = Path("EcopackAI/models/scalers/numeric_scaler.pkl")

REPORT_PATH = Path("EcopackAI/docs/encoding_normalization_report.md")

# Create folders
OUT_ENCODED_PATH.parent.mkdir(parents=True, exist_ok=True)
ENCODER_PATH.parent.mkdir(parents=True, exist_ok=True)
SCALER_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

# ------------------ LOAD CLEAN DATA ------------------
df = pd.read_csv(IN_PATH)

print("Loaded cleaned dataset:", IN_PATH)
print("Shape:", df.shape)

# ------------------ IDENTIFY FEATURES ------------------
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

print("Categorical columns:", categorical_cols)
print("Numeric columns:", numeric_cols)

# ------------------ PREPROCESSING ------------------
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
scaler = MinMaxScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", ohe, categorical_cols),
        ("num", scaler, numeric_cols)
    ],
    remainder="drop"
)

# Fit and transform
X = preprocessor.fit_transform(df)

# Get feature names
ohe_feature_names = preprocessor.named_transformers_["cat"].get_feature_names_out(categorical_cols)
final_columns = list(ohe_feature_names) + numeric_cols

df_encoded = pd.DataFrame(X, columns=final_columns)

# Save encoded dataset
df_encoded.to_csv(OUT_ENCODED_PATH, index=False)
print("Encoded dataset saved:", OUT_ENCODED_PATH)

# Save transformer objects
joblib.dump(preprocessor.named_transformers_["cat"], ENCODER_PATH)
joblib.dump(preprocessor.named_transformers_["num"], SCALER_PATH)

print("Encoder saved:", ENCODER_PATH)
print("Scaler saved:", SCALER_PATH)

# ------------------ REPORT ------------------
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("# Encoding & Normalization Report — EcoPackAI\n\n")
    f.write("## Input / Output\n")
    f.write(f"- Input cleaned dataset: `{IN_PATH}`\n")
    f.write(f"- Output encoded dataset: `{OUT_ENCODED_PATH}`\n\n")

    f.write("## Encoding Strategy\n")
    f.write("- Nominal categorical features: **One-Hot Encoding**\n")
    f.write("- Unknown categories during inference: handled with `handle_unknown='ignore'`\n\n")

    f.write("## Normalization Strategy\n")
    f.write("- Numeric features scaled using **MinMaxScaler (0–1 scaling)**\n\n")

    f.write("## Saved Artifacts\n")
    f.write(f"- OneHotEncoder saved at: `{ENCODER_PATH}`\n")
    f.write(f"- Numeric scaler saved at: `{SCALER_PATH}`\n\n")

    f.write("## Columns Encoded\n")
    f.write(f"- Total categorical columns: {len(categorical_cols)}\n")
    f.write(f"- Total numeric columns: {len(numeric_cols)}\n")
    f.write(f"- Final feature count after encoding: {df_encoded.shape[1]}\n")

print("Encoding report generated:", REPORT_PATH)
