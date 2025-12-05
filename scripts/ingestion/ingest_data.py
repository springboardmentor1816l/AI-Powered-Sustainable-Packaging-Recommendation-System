import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "db"
DB_PORT = 5432

def connect_to_db():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        print("❌ Failed to connect to DB:", e)
        return None

def recreate_material_table(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS materials;")
        cur.execute("""
            CREATE TABLE materials (
                material_id INT PRIMARY KEY,
                material_type TEXT,
                strength_mpa FLOAT,
                weight_capacity_kg FLOAT,
                biodegradability_percent FLOAT,
                co2_emission_kg_per_kg FLOAT,
                recyclability_percent FLOAT,
                cost_per_kg FLOAT,
                industry_use_case TEXT,
                source_type TEXT,
                confidence_level TEXT
            );
        """)
        conn.commit()

def insert_materials(conn, df):
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO materials (
                    material_id, material_type, strength_mpa, weight_capacity_kg,
                    biodegradability_percent, co2_emission_kg_per_kg,
                    recyclability_percent, cost_per_kg,
                    industry_use_case, source_type, confidence_level
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))
        conn.commit()

def main():
    conn = connect_to_db()
    if conn is None:
        return

    recreate_material_table(conn)

    material_df = pd.read_csv("data/raw_datasets/material_dataset.csv")
    insert_materials(conn, material_df)

    conn.close()
    print("✅ Material data successfully ingested!")

if __name__ == "__main__":
    main()
