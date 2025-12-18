import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
PRODUCT_PATH = Path("../../data/processed/product_cleaned.csv")
MATERIAL_PATH = Path("../../data/processed/material_cleaned.csv")

OUT_DIR = Path("../../data/integrated")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT_DIR / "integrated_dataset.csv"
PARQUET_OUT = "../../data/final/integrated_dataset.parquet"

# -------------------------------------------------
# Load cleaned datasets
# -------------------------------------------------
products = pd.read_csv(PRODUCT_PATH)
materials = pd.read_csv(MATERIAL_PATH)

# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def safe_lower(x):
    return str(x).strip().lower()

def category_match_flag(product_category, material_categories):
    product_category = safe_lower(product_category)
    material_categories = safe_lower(material_categories)

    category_mapping = {
        "food": ["food", "beverage"],
        "pharmacy": ["pharma", "pharmaceutical"],
        "cosmetics": ["cosmetic", "fragile"],
        "electronics": ["electronic"],
        "drinkware": ["consumer"],
        "paper product": ["low-value", "consumer"]
    }

    keywords = category_mapping.get(product_category, [product_category])
    return int(any(k in material_categories for k in keywords))

# -------------------------------------------------
# Integration process
# -------------------------------------------------
rows = []

for _, p in products.iterrows():

    # -----------------------------
    # Rule 1: Load feasibility
    # -----------------------------
    feasible = materials[
        materials["load_handling_score"] >= p["product_weight_kg"]
    ].copy()

    # -----------------------------
    # Rule 2: Fragility feasibility (1–5 scale)
    # -----------------------------
    fragility = p["fragility_index"]

    if fragility >= 4:
        feasible = feasible[
            (feasible["moisture_resistance_score"] >= 4) &
            (feasible["thermal_resistance_score"] >= 4)
        ].copy()
    elif fragility == 3:
        feasible = feasible[
            (feasible["moisture_resistance_score"] >= 3) |
            (feasible["thermal_resistance_score"] >= 3)
        ].copy()
    # fragility 1–2 → no extra constraint

    # -----------------------------
    # Combine rows (NO more filtering)
    # -----------------------------
    for _, m in feasible.iterrows():

        row = {}

        # Product fields
        for col, val in p.items():
            row[f"{col}"] = val

        # Material fields
        for col, val in m.items():
            row[f"{col}"] = val

        # Soft compatibility signal
        row["category_match_flag"] = category_match_flag(
            p["category"],
            m["suitable_product_categories"]
        )

        rows.append(row)

# -------------------------------------------------
# Build integrated dataset
# -------------------------------------------------
integrated_df = pd.DataFrame(rows)

# -------------------------------------------------
# Save outputs
# -------------------------------------------------
integrated_df.to_csv(CSV_OUT, index=False)
integrated_df.to_parquet(PARQUET_OUT, index=False)

print("Integrated dataset created successfully")
print(f"Rows: {integrated_df.shape[0]}, Columns: {integrated_df.shape[1]}")
