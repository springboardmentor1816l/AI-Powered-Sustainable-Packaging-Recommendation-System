import pandas as pd

# -----------------------------
# 1. Load cleaned datasets
# -----------------------------
materials = pd.read_csv("data/materials_clean.csv")
products = pd.read_csv("data/products_clean.csv")

# -----------------------------
# 2. Normalize text columns
# -----------------------------
materials["recommended_packaging_use_cases"] = (
    materials["recommended_packaging_use_cases"]
    .astype(str)
    .str.lower()
)

products["category"] = (
    products["category"]
    .astype(str)
    .str.lower()
)

# -----------------------------
# 3. Category → Use-case mapping
# -----------------------------
CATEGORY_USECASE_MAP = {
    "food": ["food", "fresh", "produce", "packaging"],
    "electronics": ["electronics", "protection", "device"],
    "cosmetics": ["cosmetic", "beauty"],
    "pharma": ["pharma", "medical", "blister"]
}

# -----------------------------
# 4. Business-logic integration
# -----------------------------
integrated_rows = []

for _, p in products.iterrows():
    product_category = p["category"]

    keywords = CATEGORY_USECASE_MAP.get(product_category, [])

    for _, m in materials.iterrows():
        use_case_text = m["recommended_packaging_use_cases"]

        if any(k in use_case_text for k in keywords):
            row = {**p.to_dict(), **m.to_dict()}
            integrated_rows.append(row)

integrated_df = pd.DataFrame(integrated_rows)

# -----------------------------
# 5. Save integrated dataset
# -----------------------------
integrated_df.to_csv("data/integrated_dataset.csv", index=False)

print("✅ Datasets integrated using category–use-case mapping")
print("Final shape:", integrated_df.shape)

