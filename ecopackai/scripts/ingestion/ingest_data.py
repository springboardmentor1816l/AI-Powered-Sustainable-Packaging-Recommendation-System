import psycopg2
import pandas as pd

# Folder where cleaned CSVs are stored
PROCESSED_FOLDER = "data/processed/"

# Database credentials (update later if needed)
DB_CONFIG = {
    "dbname": "ecopackai_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def insert_materials(cursor):
    df = pd.read_csv(PROCESSED_FOLDER + "material_dataset.csv")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO materials(
                material_type,
                strength_mpa,
                weight_capacity,
                biodegradability_percent,
                co2_emission_score,
                recyclability_percent,
                cost_per_kg,
                industry_use_case
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, tuple(row.values))

def insert_products(cursor):
    df = pd.read_csv(PROCESSED_FOLDER + "product_dataset.csv")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO products(
                product_name,
                category,
                product_weight,
                fragility_index,
                shipping_type
            )
            VALUES (%s,%s,%s,%s,%s)
        """, tuple(row.values))

def run_ingestion():
    conn = connect_db()
    cursor = conn.cursor()

    print(" Inserting materials...")
    insert_materials(cursor)

    print(" Inserting products...")
    insert_products(cursor)

    conn.commit()
    cursor.close()
    conn.close()

    print("Ingestion complete! All data inserted into PostgreSQL.")

if __name__ == "__main__":
    run_ingestion()
