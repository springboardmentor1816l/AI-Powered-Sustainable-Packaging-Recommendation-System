import pandas as pd

# ---------------- MATERIALS ----------------
materials = pd.read_csv(
    "EcopackAI/data/raw_datasets/materials/materials_raw.csv"
)

print("Materials Info")
print(materials.info())
print(materials.isnull().sum())

# standardize column names
materials.columns = (
    materials.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
)

# drop duplicates
materials.drop_duplicates(inplace=True)

# save cleaned file
materials.to_csv(
    "EcopackAI/data/processed/materials.csv",
    index=False
)

# ---------------- PRODUCTS ----------------
products = pd.read_csv(
    "EcopackAI/data/raw_datasets/products/products_raw.csv"
)

print("\nProducts Info")
print(products.info())
print(products.isnull().sum())

products.columns = (
    products.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
)

products.drop_duplicates(inplace=True)

products.to_csv(
    "EcopackAI/data/processed/products.csv",
    index=False
)

print("\n Validation & cleaning completed")