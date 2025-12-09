import psycopg2
import pandas as pd

# -----------------------------
# CONNECT TO POSTGRES (Docker)
# -----------------------------
try:
    conn = psycopg2.connect(
        dbname="ecopack_db",      # MUST match POSTGRES_DB in docker-compose
        user="postgres",
        password="ecopass",       # MUST match POSTGRES_PASSWORD
        host="db",                # Docker service name, not localhost
        port="5432"
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL successfully")
except Exception as e:
    print("❌ Database connection error:", e)
    exit()


# -----------------------------
# LOAD CLEANED CSV FILES
# -----------------------------
try:
    materials = pd.read_csv("../../data/processed/clean_materials.csv")
    products = pd.read_csv("../../data/processed/clean_products.csv")
    print("📄 CSV files loaded successfully")
except Exception as e:
    print("❌ Error loading CSV files:", e)
    cursor.close()
    conn.close()
    exit()


# -----------------------------
# INSERT MATERIALS
# -----------------------------
try:
    for _, row in materials.iterrows():
        cursor.execute("""
            INSERT INTO materials (
                material_id, material_name, density, cost_per_kg,
                recyclability_percent, biodegradability_percent,
                co2_factor, industry_use_case
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (material_id) DO NOTHING;
        """, (
            row["material_id"],
            row["material_name"],
            row["density"],
            row["cost_per_kg"],
            row["recyclability_percent"],
            row["biodegradability_percent"],
            row["co2_factor"],
            row["industry_use_case"]
        ))
    print("🟢 Materials inserted successfully")
except Exception as e:
    print("❌ Error inserting materials:", e)


# -----------------------------
# INSERT PRODUCTS
# -----------------------------
try:
    for _, row in products.iterrows():
        cursor.execute("""
            INSERT INTO products (
                product_name, length, width, height,
                weight, fragility
            ) VALUES (%s,%s,%s,%s,%s,%s);
        """, (
            row["product_name"],
            row["length"],
            row["width"],
            row["height"],
            row["weight"],
            row["fragility"]
        ))
    print("🟢 Products inserted successfully")
except Exception as e:
    print("❌ Error inserting products:", e)


# -----------------------------
# FINALIZE
# -----------------------------
conn.commit()
cursor.close()
conn.close()

print("🎉 Data successfully ingested into PostgreSQL")
