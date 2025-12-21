import pandas as pd

PRODUCTS_PATH = "data/processed/products_cleaned.csv"
MATERIALS_PATH = "data/processed/cleaned_dataset.csv"
OUT_PATH = "data/integrated/product_material_integrated.csv"

def integrate():
    products = pd.read_csv(PRODUCTS_PATH)
    materials = pd.read_csv(MATERIALS_PATH)

    print("Products shape:", products.shape)
    print("Materials shape:", materials.shape)

    # Cross join (Cartesian product)
    integrated = products.merge(materials, how="cross")

    print("Integrated dataset shape:", integrated.shape)

    integrated.to_csv(OUT_PATH, index=False)
    print("Saved:", OUT_PATH)

if __name__ == "__main__":
    integrate()
