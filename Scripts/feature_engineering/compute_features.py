import pandas as pd

df = pd.read_csv("data/model_ready(2)/materials_final_encoded.csv")

df["CII"] = (
    (1 - df["co2_emission_score"]) * 0.5 +
    df["biodegradability_percent"] * 0.25 +
    df["recyclability_percent"] * 0.25
) * 100

df["CEI"] = (
    (1 - df["cost_per_kg"]) * 0.7 +
    df["strength_mpa"] * 0.3
) * 100

df["MSS"] = (
    df["strength_mpa"] * 0.4 +
    df["weight_capacity"] * 0.3 +
    df["recyclability_percent"] * 0.3
) * 100

df.to_csv("data/model_ready(2)/materials_engineered.csv", index=False)
print("Features engineered")
