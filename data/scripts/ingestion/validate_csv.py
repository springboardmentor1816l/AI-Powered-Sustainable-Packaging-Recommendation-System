import pandas as pd
from pathlib import Path

# Paths
RAW = Path("data/raw_datasets")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

def validate_and_clean_materials():
    path = RAW / "materials" / "materials.csv"
    df = pd.read_csv(path)

    print("\n=== MATERIALS CSV INFO ===")
    print(df.info())
    print("\nMissing values:")
    print(df.isnull().sum())

    # Make column names consistent
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Convert columns to numeric where needed
    numeric_cols = ["density", "cost_per_kg", "recyclability_percent",
                    "biodegradability_percent", "co2_factor"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing important numeric values
    df = df.dropna(subset=["cost_per_kg", "density"])

    # Save cleaned file
    out = PROCESSED / "materials_clean.csv"
    df.to_csv(out, index=False)
    print(f"\nSaved cleaned materials to {out}")

    return df

def validate_and_clean_products():
    path = RAW / "products" / "products.csv"
    df = pd.read_csv(path)

    print("\n=== PRODUCTS CSV INFO ===")
    print(df.info())
    print("\nMissing values:")
    print(df.isnull().sum())

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    numeric_cols = ["weight", "fragility", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove any negative values (if exist)
    df = df[df["weight"] >= 0]

    # Save cleaned file
    out = PROCESSED / "products_clean.csv"
    df.to_csv(out, index=False)
    print(f"\nSaved cleaned products to {out}")

    return df

if __name__ == "__main__":
    validate_and_clean_materials()
    validate_and_clean_products()
    print("\nValidation + Cleaning Completed ✔")
