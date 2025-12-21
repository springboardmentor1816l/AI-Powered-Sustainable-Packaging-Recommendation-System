import pandas as pd
import os

RAW_PATH = "data/raw_datasets/product_dataset.csv"
OUTPUT_PATH = "data/processed/products_cleaned.csv"

def clean_products():
    df = pd.read_csv(RAW_PATH)

    print(f"Initial shape: {df.shape}")

    # -----------------------------
    # 1. Remove duplicate rows
    # -----------------------------
    df = df.drop_duplicates()

    # -----------------------------
    # 2. Handle missing values
    # -----------------------------

    # Numeric columns
    numeric_cols = [
        "product_weight_kg",
        "fragility_index"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Categorical columns
    categorical_cols = [
        "product_name",
        "category",
        "shipping_type"
    ]

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # -----------------------------
    # 3. Basic validation
    # -----------------------------
    df = df[df["product_weight_kg"] > 0]
    df = df[df["fragility_index"].between(1, 10)]

    # -----------------------------
    # 4. Save cleaned dataset
    # -----------------------------
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Cleaned shape: {df.shape}")
    print(f"Saved cleaned products to: {OUTPUT_PATH}")

if __name__ == "__main__":
    clean_products()
