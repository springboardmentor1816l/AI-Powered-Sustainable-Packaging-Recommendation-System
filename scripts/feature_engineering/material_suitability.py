import pandas as pd
from pathlib import Path

# -------------------------
# PATHS
# -------------------------
IN_PATH = "data/integrated/product_material_integrated.csv"
OUT_PATH = "data/engineered/integrated_with_suitability.csv"

Path("data/engineered").mkdir(parents=True, exist_ok=True)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(IN_PATH)

# -------------------------
# NORMALIZATION HELPERS
# -------------------------
def normalize(series, min_val=0, max_val=10):
    return (series - min_val) / (max_val - min_val)

# -------------------------
# SCORE CALCULATION
# -------------------------
load_score = normalize(df["Load Handling Score"])
moisture_score = normalize(df["Moisture Resistance Score"])
thermal_score = normalize(df["Thermal Resistance Score"])

# Fragility compatibility (lower fragility = easier material fit)
fragility_match = 1 - normalize(df["fragility_index"])

# -------------------------
# FINAL SUITABILITY SCORE
# -------------------------
df["Material Suitability Score"] = (
    0.30 * load_score +
    0.25 * moisture_score +
    0.25 * thermal_score +
    0.20 * fragility_match
) * 100

df["Material Suitability Score"] = df["Material Suitability Score"].round(2)

# -------------------------
# SAVE
# -------------------------
df.to_csv(OUT_PATH, index=False)

print("✅ Material Suitability Score generated")
print(f"Saved to → {OUT_PATH}")
