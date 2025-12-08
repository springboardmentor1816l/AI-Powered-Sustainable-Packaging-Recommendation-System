import psycopg2
import pandas as pd
from pathlib import Path

CLEAN = Path("data/processed")

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "snehaldnyane@2005",   
    "host": "localhost",
    "port": 5432
}


def connect_db():
    return psycopg2.connect(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )

def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            material_name VARCHAR(255),
            density FLOAT,
            cost_per_kg FLOAT,
            recyclability_percent FLOAT,
            biodegradability_percent FLOAT,
            co2_factor FLOAT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(255),
            weight FLOAT,
            fragility INT,
            volume FLOAT,
            category VARCHAR(255),
            shipping_type VARCHAR(255)
        );
    """)

    conn.commit()
    cur.close()
    print("Tables created successfully ")

def log_audit(conn, operation, table_name, row_count, status):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO audit_logs (operation, table_name, row_count, status)
        VALUES (%s, %s, %s, %s)
    """, (operation, table_name, row_count, status))
    conn.commit()
    cur.close()

def insert_materials(conn):
    df = pd.read_csv(CLEAN / "materials_clean.csv")
    cur = conn.cursor()
    log_audit(conn, "DATA_INGESTION", "materials", len(df), "SUCCESS")


    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO materials
            (material_name, density, cost_per_kg, recyclability_percent, biodegradability_percent, co2_factor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row["material_name"],
            row["density"],
            row["cost_per_kg"],
            row["recyclability_percent"],
            row["biodegradability_percent"],
            row["co2_factor"]
        ))

def insert_products(conn):
    df = pd.read_csv(CLEAN / "products_clean.csv")
    cur = conn.cursor()
    log_audit(conn, "DATA_INGESTION", "products", len(df), "SUCCESS")


    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO products
            (product_name, weight, fragility, volume, category, shipping_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row["product_name"],
            row["weight"],
            row["fragility"],
            row["volume"],
            row["category"],
            row["shipping_type"]
        ))

    conn.commit()
    cur.close()
    print("Inserted products ")

if __name__ == "__main__":
    print("Connecting to database...")
    conn = connect_db()

    create_tables(conn)
    insert_materials(conn)
    insert_products(conn)

    conn.close()
    print("\nData Ingestion Completed Successfully ")
