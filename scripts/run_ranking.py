import pandas as pd
from src.recommendation.ranker import rank_materials

# INPUT (example combined predictions)
df = pd.read_csv("data/final/material_predictions.csv")

ranked = rank_materials(df)

ranked.to_csv("outputs/material_rankings.csv", index=False)

print("✅ Material ranking completed")
