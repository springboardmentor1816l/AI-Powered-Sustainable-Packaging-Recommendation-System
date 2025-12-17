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

# DB CONNECT
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

print("🔗 Connected to database.")

# ------------ MATERIALS INGESTION ------------
print("\n📦 Ingesting materials.csv ...")

materials_df = pd.read_csv(os.path.join(processed_path, files["materials"]))

for _, row in materials_df.iterrows():
    cursor.execute("""
    INSERT INTO materials (
        material_type, strength_mpa, weight_capacity, biodegradability_percent,
        co2_emission_score, recyclability_percent, cost_per_kg, industry_use_case
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row['material_type'], row['strength_mpa'], row['weight_capacity'],
        row['biodegradability_percent'], row['co2_emission_score'], 
        row['recyclability_percent'], row['cost_per_kg'], row['industry_use_case']
    ))

print("✔ Materials data inserted.")


# ------------ PRODUCTS INGESTION ------------
print("\n📦 Ingesting products.csv ...")

products_df = pd.read_csv(os.path.join(processed_path, files["products"]))

for _, row in products_df.iterrows():
    cursor.execute("""
    INSERT INTO products (
        product_name, category, product_weight, fragility_index, shipping_type
    ) VALUES (%s,%s,%s,%s,%s)
    """, (
        row['product_name'], row['category'], row['product_weight'],
        row['fragility_index'], row['shipping_type']
    ))

print("✔ Products data inserted.")

conn.commit()
cursor.close()
conn.close()

print("\n🎉 Data ingestion completed successfully!")
