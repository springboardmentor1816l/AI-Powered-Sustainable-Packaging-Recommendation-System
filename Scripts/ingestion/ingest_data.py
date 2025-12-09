import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ---------- 1. DB CONFIG — CHANGE THESE TO YOUR REAL VALUES ----------
DB_NAME = "ecopack"      # make sure this database exists
DB_USER = "postgres"     # or "admin" if you created that user
DB_PASSWORD = "2808"
DB_HOST = "localhost"
DB_PORT = 5432           # default PostgreSQL port

# ---------- 2. HELPER: CONNECT TO DB ----------
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        print(f"[DB ERROR] Could not connect to database: {e}")
        raise

# ---------- 3. GENERIC FUNCTION TO INGEST A CSV ----------
def ingest_csv_to_table(csv_path, table_name):
    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        return

    print(f"\n[INFO] Ingesting {csv_path} -> {table_name}")

    # Read CSV
    df = pd.read_csv(csv_path)

    if df.empty:
        print(f"[WARN] {csv_path} is empty. Skipping.")
        return

    # Replace NaN with None so psycopg2 can handle NULLs
    df = df.where(pd.notnull(df), None)

    # Get column names from CSV (must match table columns in DB)
    columns = list(df.columns)
    print(f"[INFO] Columns: {columns}")

    col_names = ", ".join(columns)
    insert_query = f"INSERT INTO {table_name} ({col_names}) VALUES %s"

    # Convert DataFrame rows to list of tuples
    rows = [tuple(x) for x in df.to_numpy()]

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        execute_values(cur, insert_query, rows)
        conn.commit()
        cur.close()
        print(f"[SUCCESS] Inserted {len(rows)} rows into {table_name}")
    except Exception as e:
        print(f"[ERROR] Failed to insert into {table_name}: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

# ---------- 4. MAIN EXECUTION ----------
if __name__ == "__main__":
    # BASE_DIR: project root: AI-Powered-Sustainable-Packaging-Recommendation-System
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    processed_dir = os.path.join(BASE_DIR, "data", "processed")

    # CSV -> table mappings
    tasks = [
        ("materials.csv", "materials"),
        ("products.csv", "products"),
        # add more here if needed
        # ("co2_factors.csv", "co2_factors"),
    ]

    for csv_file, table in tasks:
        csv_path = os.path.join(processed_dir, csv_file)
        ingest_csv_to_table(csv_path, table)

    print("\n[DONE] Ingestion script finished.")

