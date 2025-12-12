# scripts/processing/feature_engineering.py
import os, json, numpy as np, pandas as pd
from pathlib import Path

# --- CONFIG (default weights) ---
CII_WEIGHTS = {"co2": 0.6, "biodeg": 0.1, "recy": 0.3}

CEI_WEIGHTS = {"cost": 0.6, "dur": 0.3, "recy_bonus": 0.1}
MSS_WEIGHTS = {"load": 0.25, "moisture": 0.2, "thermal": 0.2, "dur": 0.25, "category": 0.1}
RECY_MAP = {"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25}

# Paths
RAW = Path("data/raw/EcoPackAI_dataset.csv")
PROCESSED = Path("data/processed"); PROCESSED.mkdir(parents=True, exist_ok=True)
DOCS = Path("docs"); DOCS.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(RAW)
out = df.copy()

# Helper: try several candidate column names and return the first that exists
def safe_col(candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

# Candidate names (if your columns differ, edit these lists below)
col_co2 = safe_col(["Carbon Footprint (kg CO2e/kg)", "carbon_footprint", "co2_footprint", "CO2"])
col_biodeg = safe_col(["Biodegradation Time (days)", "biodegradation_time", "biodeg_time"])
col_recy_pct = safe_col(["Recyclability (%)", "recyclability_percent", "recyclability"])
col_recy_cat = safe_col(["Recyclability Category", "recyclability_category"])
col_cost = safe_col(["cost_per_kg", "Cost per kg", "Cost_per_kg", "Cost/kg"])
col_weight_required = safe_col(["weight_required", "weight", "weight_required_per_unit", "Weight required"])
col_durability = safe_col(["durability_score", "Durability", "material_durability", "Durability Score"])
col_load = safe_col(["load_handling_score", "Load handling score", "load_score"])
col_moisture = safe_col(["moisture_resistance_score", "moisture_resistance"])
col_thermal = safe_col(["thermal_resistance_score", "thermal_resistance"])
col_product_categories = safe_col(["Suitable Product Categories", "suitable_product_categories", "Suitable_Product_Categories"])

# Helper normalization that tolerates NaNs: fill median then min-max
def safe_minmax(arr):
    a = np.array(arr, dtype=float).reshape(-1,1)
    if np.all(np.isnan(a)):
        return np.zeros_like(a)
    med = np.nanmedian(a)
    a[np.isnan(a)] = med
    denom = (np.nanmax(a) - np.nanmin(a)) if np.nanmax(a) != np.nanmin(a) else 1.0
    norm = (a - np.nanmin(a)) / denom
    return norm

# ---- Compute CII (CO2 Impact Index) ----
co2_vals = df[col_co2].astype(float).to_numpy().reshape(-1,1) if col_co2 else np.full((len(df),1), np.nan)
bd_vals = df[col_biodeg].astype(float).to_numpy().reshape(-1,1) if col_biodeg else np.full((len(df),1), np.nan)
co2_score = 1.0 - safe_minmax(co2_vals).flatten()
bd_score = 1.0 - safe_minmax(bd_vals).flatten()

if col_recy_pct:
    recy_score = df[col_recy_pct].astype(float).fillna(df[col_recy_pct].median() if df[col_recy_pct].notna().any() else 0) / 100.0
elif col_recy_cat:
    recy_score = df[col_recy_cat].map(lambda x: RECY_MAP.get(str(x).strip().upper(), 0.5)).astype(float)
else:
    recy_score = pd.Series(0.0, index=df.index)

cii_raw = (CII_WEIGHTS["co2"] * co2_score + CII_WEIGHTS["biodeg"] * bd_score + CII_WEIGHTS["recy"] * recy_score.values)
out["CII"] = np.round(np.clip(cii_raw,0,1) * 100.0, 2)

# ---- Compute CEI (Cost Efficiency Index) ----
if col_cost:
    cost_vals = df[col_cost].astype(float).fillna(df[col_cost].median() if df[col_cost].notna().any() else 0).to_numpy()
else:
    cost_vals = np.zeros(len(df))

if col_weight_required:
    weight_vals = df[col_weight_required].astype(float).fillna(df[col_weight_required].median() if df[col_weight_required].notna().any() else 1).to_numpy()
else:
    weight_guess = safe_col(["weight","package_weight","Weight"])
    if weight_guess:
        weight_vals = df[weight_guess].astype(float).fillna(df[weight_guess].median()).to_numpy()
    else:
        weight_vals = np.ones(len(df))

cost_per_unit = cost_vals * weight_vals
cost_score = 1.0 - safe_minmax(cost_per_unit).flatten()

if col_durability:
    dur_norm = safe_minmax(df[col_durability].astype(float).to_numpy().reshape(-1,1)).flatten()
else:
    dur_norm = np.zeros(len(df))

cei_raw = CEI_WEIGHTS["cost"] * cost_score + CEI_WEIGHTS["dur"] * dur_norm + CEI_WEIGHTS["recy_bonus"] * recy_score.values
out["CEI"] = np.round(np.clip(cei_raw,0,1) * 100.0, 2)

# ---- Compute MSS (Material Suitability Score) ----
load_n = safe_minmax(df[col_load].astype(float).to_numpy().reshape(-1,1)).flatten() if col_load else np.zeros(len(df))
moist_n = safe_minmax(df[col_moisture].astype(float).to_numpy().reshape(-1,1)).flatten() if col_moisture else np.zeros(len(df))
therm_n = safe_minmax(df[col_thermal].astype(float).to_numpy().reshape(-1,1)).flatten() if col_thermal else np.zeros(len(df))
dur_n = dur_norm

cat_match = np.zeros(len(df))
if col_product_categories:
    for i, val in enumerate(df[col_product_categories].fillna("")):
        cat_match[i] = 1.0 if str(val).strip() else 0.0

mss_raw = (MSS_WEIGHTS["load"]*load_n + MSS_WEIGHTS["moisture"]*moist_n + MSS_WEIGHTS["thermal"]*therm_n + MSS_WEIGHTS["dur"]*dur_n + MSS_WEIGHTS["category"]*cat_match)
out["MSS"] = np.round(np.clip(mss_raw,0,1) * 100.0, 2)

# ---- Final recommendation score (weighted) ----
FINAL_WEIGHTS = {"CII":0.4,"CEI":0.3,"MSS":0.3}
final_raw = FINAL_WEIGHTS["CII"] * out["CII"]/100.0 + FINAL_WEIGHTS["CEI"] * out["CEI"]/100.0 + FINAL_WEIGHTS["MSS"] * out["MSS"]/100.0
out["Final_Recommendation_Score"] = np.round(np.clip(final_raw,0,1)*100.0, 2)

# ---- Save outputs ----
engineered_path = PROCESSED / "engineered_features.csv"
out.to_csv(engineered_path, index=False)
print("Saved engineered features ->", engineered_path)

metadata = {
 "CII":{"inputs":[col_co2,col_biodeg,col_recy_pct or col_recy_cat],"weights":CII_WEIGHTS},
 "CEI":{"inputs":[col_cost,col_weight_required,col_durability],"weights":CEI_WEIGHTS},
 "MSS":{"inputs":[col_load,col_moisture,col_thermal,col_durability,col_product_categories],"weights":MSS_WEIGHTS}
}
with open(PROCESSED/"feature_metadata.json","w") as f:
    json.dump(metadata, f, indent=2)

Path("docs/feature_engineering_document.md").write_text("Feature engineering document saved.")
Path("docs/feature_transformation_plan.md").write_text("Feature transformation plan saved.")
print("Saved docs & metadata.")
