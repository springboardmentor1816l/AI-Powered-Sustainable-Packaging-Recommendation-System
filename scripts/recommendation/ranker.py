import pandas as pd
from pathlib import Path

# -------------------------
# Paths
# -------------------------
INPUT_PATH = "data/final/material_recommendations.csv"
OUTPUT_PATH = "outputs/material_rankings.csv"

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(INPUT_PATH)

# -------------------------
# SAFETY CHECK (IMPORTANT)
# -------------------------
# If already ranked, do NOT re-rank
REQUIRED_FINAL_COLS = {"material", "final_score"}

if REQUIRED_FINAL_COLS.issubset(df.columns):
    print("✅ Detected already-ranked material recommendations.")
    print("ℹ️ Skipping ranking step.")
    print(df.head())

    Path("outputs").mkdir(exist_ok=True, parents=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"📁 Final rankings saved to: {OUTPUT_PATH}")
    exit(0)

# -------------------------
# (This block will NEVER run in your current pipeline)
# -------------------------
raise RuntimeError(
    "❌ Ranking expects prediction-level input, "
    "but received an unsupported schema."
)
