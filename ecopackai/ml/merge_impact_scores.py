import pandas as pd

# Load both datasets
cost = pd.read_csv("data/integrated_with_cost_score.csv")
co2  = pd.read_csv("data/integrated_with_co2_score.csv")

# Reset index to guarantee row alignment
cost = cost.reset_index(drop=True)
co2  = co2.reset_index(drop=True)

# Attach scores
co2["cost_impact_score"] = cost["cost_impact_score"]

# Save merged dataset
co2.to_csv("data/integrated_with_all_scores.csv", index=False)

print("✅ CO₂ and Cost impact scores merged successfully")
print("Columns now include:")
print(co2[["co2_impact_score", "cost_impact_score"]].head())
