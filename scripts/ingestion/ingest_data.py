import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env (local dev only)
load_dotenv()

# Database connection parameters (NO hardcoding)
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# CSV paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

MATERIALS_CSV = os.path.join(PROCESSED_DIR, "material_dataset.csv")
PRODUCTS_CSV = os.path.join(PROCESSED_DIR, "product_dataset.csv")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def ingest_materials(conn):
    df = pd.read_csv(MATERIALS_CSV)

    insert_query = """
        INSERT INTO materials (
            material_id, material_type, strength_mpa, weight_capacity,
            biodegradability_percent, co2_emission_score,
            recyclability_percent, cost_per_kg, industry_use_case
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (material_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
    conn.commit()

def ingest_products(conn):
    df = pd.read_csv(PRODUCTS_CSV)

    insert_query = """
        INSERT INTO products (
            product_id, product_name, category,
            product_weight, fragility_index, shipping_type
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
    conn.commit()

def main():
    conn = get_connection()
    try:
        ingest_materials(conn)
        ingest_products(conn)
        print("Data ingestion completed successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
