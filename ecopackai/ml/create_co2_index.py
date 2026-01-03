import pandas as pd

df = pd.read_csv("data/integrated_dataset_final_pdf.csv")

# Quantile-based CO2 impact index (LOW / MEDIUM / HIGH)
df["co2_impact_index"] = pd.qcut(
    df["co2_emission_score"],
    q=3,
    labels=[0, 1, 2]
)

df.to_csv("data/integrated_with_co2_index.csv", index=False)

print("✅ CO₂ Impact Index created")
print(df["co2_impact_index"].value_counts())
