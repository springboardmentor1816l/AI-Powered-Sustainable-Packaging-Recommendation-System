import pandas as pd

materials = pd.read_csv("data/model_ready(2)/materials_engineered.csv")
products = pd.read_csv("data/processed(1)/products_updated.csv")

materials["_k"] = 1
products["_k"] = 1

combined = pd.merge(products, materials, on="_k").drop("_k", axis=1)

combined.to_csv(
    "data/combined(3)/combined_products_materials.csv",
    index=False
)

print("Combined dataset created")
