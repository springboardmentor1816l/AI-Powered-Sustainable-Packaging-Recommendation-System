import pandas as pd
import psycopg2
import os

DB_NAME = "ecopack_db"
DB_USER = "ecopack"
DB_PASSWORD = "ecopack123"
DB_HOST = "localhost"
DB_PORT = "5432"

processed_path = "data/processed/"

files = {
    "materials": "material_dataset.csv",
    "products": "product_dataset.csv"
}

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("🔗 Connected to PostgreSQL successfully!")
except Exception as e:
    print("❌ Database connection failed:", e)
    exit()

# ---------------- INSERT MATERIALS ----------------
print("\n📦 Importing materials...")

materials_df = pd.read_csv(os.path.join(processed_path, files["materials"]))

for _, row in materials_df.iterrows():
    cursor.execute("""
        INSERT INTO materials (
            material_type, strength_mpa, weight_capacity, biodegradability_percent,
            co2_emission_score, recyclability_percent, cost_per_kg, industry_use_case
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """, tuple(row))

print("✔ Materials table updated!")


# ---------------- INSERT PRODUCTS ----------------
print("\n📦 Importing products...")

products_df = pd.read_csv(os.path.join(processed_path, files["products"]))

for _, row in products_df.iterrows():
    cursor.execute("""
        INSERT INTO products (
            product_name, category, product_weight, fragility_index, shipping_type
        ) VALUES (%s,%s,%s,%s,%s);
    """, tuple(row))

print("✔ Products table updated!")

conn.commit()
cursor.close()
conn.close()

print("\n🎉 DATA IMPORT COMPLETE!")
