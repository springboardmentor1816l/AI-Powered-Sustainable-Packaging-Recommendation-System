import os
import pandas as pd
import psycopg2

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # project root
RAW_DIR = os.path.join(BASE_DIR, "data", "raw_datasets")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

MATERIALS_RAW = os.path.join(RAW_DIR, "materials.csv")
PRODUCTS_RAW = os.path.join(RAW_DIR, "products.csv")

MATERIALS_CLEAN = os.path.join(PROCESSED_DIR, "materials.csv")
PRODUCTS_CLEAN = os.path.join(PROCESSED_DIR, "products.csv")


# ---------- 1. LOAD RAW CSVs ----------
def load_raw_data():
    print("📥 Loading raw CSVs...")
    materials_df = pd.read_csv(MATERIALS_RAW)
    products_df = pd.read_csv(PRODUCTS_RAW)
    return materials_df, products_df


# ---------- 2. VALIDATE DATA ----------
def validate_df(name, df):
    print(f"\n====== VALIDATION: {name} ======")
    print("Shape (rows, columns):", df.shape)
    print("\nColumns and types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print("\nFirst few rows:")
    print(df.head())


# ---------- 3. CLEAN DATA (simple for now) ----------
def clean_materials(df):
    # Example cleaning: drop duplicates and rows with all NaN
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    # All column names already in snake_case and match schema
    return df


def clean_products(df):
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    return df


# ---------- 4. SAVE CLEANED CSVs ----------
def save_processed(materials_df, products_df):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    materials_df.to_csv(MATERIALS_CLEAN, index=False)
    products_df.to_csv(PRODUCTS_CLEAN, index=False)
    print(f"\n💾 Saved cleaned materials to: {MATERIALS_CLEAN}")
    print(f"💾 Saved cleaned products to:  {PRODUCTS_CLEAN}")


# ---------- 5. LOAD INTO POSTGRESQL ----------
def load_into_postgres(materials_df, products_df):
    # Connection details must match docker-compose.yml
    conn = psycopg2.connect(
        dbname="ecopackai_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()

    print("\n🔗 Connected to PostgreSQL, inserting data...")

    # Insert materials (material_id is SERIAL so we don't insert it)
    materials_query = """
        INSERT INTO materials
        (material_type, strength_mpa, weight_capacity,
         biodegradability_percent, co2_emission_score,
         recyclability_percent, cost_per_kg, industry_use_case)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in materials_df.iterrows():
        cursor.execute(
            materials_query,
            (
                row["material_type"],
                float(row["strength_mpa"]),
                float(row["weight_capacity"]),
                float(row["biodegradability_percent"]),
                float(row["co2_emission_score"]),
                float(row["recyclability_percent"]),
                float(row["cost_per_kg"]),
                row["industry_use_case"],
            ),
        )

    # Insert products (product_id is SERIAL)
    products_query = """
        INSERT INTO products
        (product_name, category, product_weight,
         fragility_index, shipping_type)
        VALUES (%s, %s, %s, %s, %s)
    """

    for _, row in products_df.iterrows():
        cursor.execute(
            products_query,
            (
                row["product_name"],
                row["category"],
                float(row["product_weight"]),
                int(row["fragility_index"]),
                row["shipping_type"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data inserted into materials and products tables.")


def main():
    # 1. Load
    materials_df, products_df = load_raw_data()

    # 2. Validate
    validate_df("RAW MATERIALS", materials_df)
    validate_df("RAW PRODUCTS", products_df)

    # 3. Clean
    materials_clean = clean_materials(materials_df)
    products_clean = clean_products(products_df)

    # 4. Save cleaned CSVs
    save_processed(materials_clean, products_clean)

    # 5. Load into Postgres
    load_into_postgres(materials_clean, products_clean)

    print("\n🎉 Ingestion pipeline completed successfully!")


if __name__ == "__main__":
    main()
