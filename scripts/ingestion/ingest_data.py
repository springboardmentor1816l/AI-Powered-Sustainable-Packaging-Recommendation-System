import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="ecopack",
    user="admin",
    password="pass",
    host="localhost"
)

cursor = conn.cursor()

df = pd.read_csv("data/processed/materials_cleaned.csv")

for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO materials(name, density, cost, eco_rating) VALUES (%s, %s, %s, %s)",
        (row['name'], row['density'], row['cost'], row['eco_rating'])
    )

conn.commit()
cursor.close()
conn.close()

print("Data ingestion completed successfully.")
