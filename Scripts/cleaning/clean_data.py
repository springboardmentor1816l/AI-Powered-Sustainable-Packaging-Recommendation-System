import pandas as pd

# Load raw data
materials = pd.read_csv("data/raw(0)/materials.csv")
products = pd.read_csv("data/raw(0)/products.csv")

# Fill missing values (example logic)
materials.fillna(materials.mean(numeric_only=True), inplace=True)
products.fillna(products.mean(numeric_only=True), inplace=True)

# Save cleaned data
materials.to_csv("data/processed(1)/materials_updated.csv", index=False)
products.to_csv("data/processed(1)/products_updated.csv", index=False)

print("✔ Cleaned datasets saved")
