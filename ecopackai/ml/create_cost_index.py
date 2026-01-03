import pandas as pd

df = pd.read_csv("data/integrated_dataset_final_pdf.csv")

df["cost_impact_index"] = pd.qcut(
    df["cost_per_unit"],
    q=3,
    labels=[0, 1, 2]
).astype(int)

df.to_csv("data/integrated_with_cost_index.csv", index=False)

print("✅ Cost Impact Index created")
print(df["cost_impact_index"].value_counts())
