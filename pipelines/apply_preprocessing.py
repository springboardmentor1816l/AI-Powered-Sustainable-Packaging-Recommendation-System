import os
import joblib
import pandas as pd

# -----------------------------
# PATHS
# -----------------------------
DATA_PATH = "data/processed/material_cleaned.csv"
PIPELINE_PATH = "models/pipelines/preprocessing_pipeline.pkl"
OUTPUT_PATH = "data/model_ready/materials_preprocessed_pipeline.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATA_PATH)

# -----------------------------
# DROP ID / TARGET COLUMNS IF PRESENT
# -----------------------------
drop_cols = [
    "material_id",
    "recommended_material",
    "sustainability_score",
    "cost_efficiency_category"
]

df_features = df.drop(columns=[c for c in drop_cols if c in df.columns])

# -----------------------------
# LOAD PIPELINE
# -----------------------------
preprocessor = joblib.load(PIPELINE_PATH)

# -----------------------------
# APPLY PIPELINE
# -----------------------------
X_transformed = preprocessor.fit_transform(df_features)

# -----------------------------
# GET FEATURE NAMES (NO BIN NOW)
# -----------------------------
num_features = preprocessor.named_transformers_["num"].get_feature_names_out()
cat_features = (
    preprocessor
    .named_transformers_["cat"]
    .named_steps["encoder"]
    .get_feature_names_out()
)

feature_names = list(num_features) + list(cat_features)

# -----------------------------
# SAVE MODEL-READY DATA
# -----------------------------
df_model_ready = pd.DataFrame(X_transformed, columns=feature_names)

os.makedirs("data/model_ready", exist_ok=True)
df_model_ready.to_csv(OUTPUT_PATH, index=False)

print("✅ Preprocessing pipeline applied successfully")
print("✅ Model-ready dataset saved at:", OUTPUT_PATH)
