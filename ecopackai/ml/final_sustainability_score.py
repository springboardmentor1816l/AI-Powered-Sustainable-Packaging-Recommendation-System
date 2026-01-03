import pandas as pd

# =========================================================
# LOAD DATA (WITH SCORES)
# =========================================================
df = pd.read_csv("data/integrated_with_all_scores.csv")
print("✅ Dataset loaded:", df.shape)

# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================
REQUIRED_COLS = [
    "co2_impact_score",
    "cost_impact_score",
    "material_suitability_score"
]

missing = [c for c in REQUIRED_COLS if c not in df.columns]
if missing:
    raise ValueError(f"❌ Missing required columns: {missing}")

# =========================================================
# FINAL SUSTAINABILITY SCORE (WEIGHTED FUSION)
# =========================================================
df["final_sustainability_score"] = (
    0.45 * df["co2_impact_score"] +
    0.35 * df["cost_impact_score"] +
    0.20 * df["material_suitability_score"]
)

# =========================================================
# NORMALIZE TO 0–1
# =========================================================
df["final_sustainability_score"] = (
    (df["final_sustainability_score"] - df["final_sustainability_score"].min()) /
    (df["final_sustainability_score"].max() - df["final_sustainability_score"].min())
)

# =========================================================
# SAVE FINAL DATASET
# =========================================================
OUTPUT_PATH = "data/final_sustainability_scores.csv"
df.to_csv(OUTPUT_PATH, index=False)

print("💾 Final sustainability scores saved to:", OUTPUT_PATH)

# =========================================================
# SANITY CHECK
# =========================================================
print("\n📊 FINAL SUSTAINABILITY SCORE STATS")
print(df["final_sustainability_score"].describe())
