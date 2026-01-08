import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="ecopack",
    user="admin",
    password="pass",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

materials_df = pd.read_csv('./data/processed/materials_cleaned.csv')

for _, row in materials_df.iterrows():
    cursor.execute("""
        INSERT INTO materials(name, density, cost)
        VALUES (%s, %s, %s);
    """, (row['name'], row['density'], row['cost']))

print("Materials inserted.")

products_df = pd.read_csv('./data/processed/products_cleaned.csv')

for _, row in products_df.iterrows():
    cursor.execute("""
        INSERT INTO products(name, length, width, height, fragility)
        VALUES (%s, %s, %s, %s, %s);
    """, (row['name'], row['length'], row['width'], row['height'], row['fragility']))

print("Products inserted.")

conn.commit()
cursor.close()
conn.close()

print("Ingestion Completed Successfully.")
