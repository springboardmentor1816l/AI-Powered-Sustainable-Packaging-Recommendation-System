import pandas as pd
import os

# --------------------------------------------------
# LOAD SINGLE SOURCE OF TRUTH
# --------------------------------------------------
df = pd.read_csv(
    "data/combined(3)/combined_products_materials.csv"
)

# --------------------------------------------------
# DEFINE TARGETS (PDF REQUIRED)
# --------------------------------------------------
target_cols = [
    "cost_per_kg",
    "co2_emission_score"
]

# --------------------------------------------------
# BUILD y_raw (NUMERIC ONLY)
# --------------------------------------------------
y = df[target_cols]

# --------------------------------------------------
# BUILD X_raw (DROP TARGETS + IDS)
# --------------------------------------------------
id_cols = [
    "material_id",
    "product_id"
]

X = df.drop(columns=target_cols + id_cols, errors="ignore")

# --------------------------------------------------
# OUTPUT FOLDER
# --------------------------------------------------
OUT_DIR = "data/model_ready(2)"
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------
# SAVE FILES
# --------------------------------------------------
X.to_csv(f"{OUT_DIR}/X_raw.csv", index=False)
y.to_csv(f"{OUT_DIR}/y_raw.csv", index=False)

print("X_raw and y_raw rebuilt correctly")
print("Rows in X:", len(X))
print("Rows in y:", len(y))
