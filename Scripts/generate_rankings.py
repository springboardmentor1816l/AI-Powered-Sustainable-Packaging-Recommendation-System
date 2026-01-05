import sys
from pathlib import Path
import pandas as pd
import os

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.recommendation.ranker import rank_materials

df = pd.read_parquet("data/model_ready/combined_model_ready.parquet")

ranked = rank_materials(df)

# ✅ ensure output folder exists
os.makedirs("outputs", exist_ok=True)

ranked.to_csv("outputs/material_rankings.csv", index=False)

print("✅ Material rankings generated")

