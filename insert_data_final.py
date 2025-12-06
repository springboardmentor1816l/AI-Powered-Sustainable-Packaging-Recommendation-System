import mysql.connector
import pandas as pd

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tanmay@123",
        database="ecopackai_db"
    )
    cursor = conn.cursor()
    print("Connected to MySQL.")

    # Load CSVs
    material_df = pd.read_csv(r"C:\Users\Tanmay\AI-Powered-Sustainable-Packaging-Recommendation-System\data\material_dataset.csv")
    product_df = pd.read_csv(r"C:\Users\Tanmay\AI-Powered-Sustainable-Packaging-Recommendation-System\data\product_dataset.csv")

    print("Material CSV shape:", material_df.shape)
    print("Product CSV shape :", product_df.shape)

    # -------------------------
    # INSERT MATERIALS
    # -------------------------
    material_query = """
        INSERT INTO materials 
        (material_type, strength_mpa, weight_capacity, biodegradability_percent,
         co2_emission_score, recyclability_percent, cost_per_kg, industry_use_case)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in material_df.iterrows():
        cursor.execute(material_query, (
            row['material_type'],
            row['strength_mpa'],
            row['weight_capacity_kg'],
            row['biodegradability_percent'],
            row['co2_emission_kg_per_kg'],
            row['recyclability_percent'],
            row['cost_per_kg'],
            row['industry_use_case']
        ))

    conn.commit()
    print("Inserted materials:", len(material_df))

    # -------------------------
    # INSERT PRODUCTS (CSV COLUMNS FIXED)
    # -------------------------
    product_query = """
        INSERT INTO products
        (product_id, product_name, category, product_weight, fragility_index, shipping_type)
        VALUES (%s,%s,%s,%s,%s,%s)
    """

    for _, row in product_df.iterrows():
        cursor.execute(product_query, (
            row['product_id'],
            row['product_name'],
            row['category'],
            row['product_weight'],  # <-- FIXED (matches CSV column name)
            row['fragility_index'],
            row['shipping_type']
        ))

    conn.commit()
    print("Inserted products:", len(product_df))

    print("ALL DATA INSERTED SUCCESSFULLY!")

except Exception as e:
    print("Error:", e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
