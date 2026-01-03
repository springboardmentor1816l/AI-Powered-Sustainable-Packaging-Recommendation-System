import pandas as pd

df = pd.read_csv("data/integrated_dataset_final_pdf.csv")

print("Shape:", df.shape)
print("\nColumns:")
for c in df.columns:
    print("-", c)

print("\nMissing values:")
print(df.isna().sum())
