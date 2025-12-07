import pandas as pd
import pymysql

DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "127.0.0.1"
DB_PORT = 3306

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

def import_materials():
    print("Reading materials.csv...")
    df = pd.read_csv("data/processed/materials.csv")

    conn = get_connection()
    cur = conn.cursor()

    print("Inserting materials...")
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO materials (
                material_type, strength_mpa, weight_capacity,
                biodegradability_percent, co2_emission_score,
                recyclability_percent, cost_per_kg, industry_use_case
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["material_type"], row["strength_mpa"], row["weight_capacity"],
            row["biodegradability_percent"], row["co2_emission_score"],
            row["recyclability_percent"], row["cost_per_kg"], row["industry_use_case"]
        ))

    conn.commit()
    conn.close()
    print("Materials imported successfully!\n")


def import_products():
    print("Reading products.csv...")
    df = pd.read_csv("data/processed/products.csv")

    conn = get_connection()
    cur = conn.cursor()

    print("Inserting products...")
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO products (
                product_name, category, product_weight,
                fragility_index, shipping_type
            )
            VALUES (%s,%s,%s,%s,%s)
        """, (
            row["product_name"], row["category"], row["product_weight"],
            row["fragility_index"], row["shipping_type"]
        ))

    conn.commit()
    conn.close()
    print("Products imported successfully!\n")


if __name__ == "__main__":
    import_materials()
    import_products()
