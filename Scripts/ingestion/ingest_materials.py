import pandas as pd
from db_config import get_connection

df = pd.read_csv("data/processed(1)/materials_updated.csv")

conn = get_connection()
cur = conn.cursor()

# 🔥 Clear existing data
cur.execute("TRUNCATE TABLE materials RESTART IDENTITY CASCADE;")

for _, row in df.iterrows():
    cur.execute(
        """
        INSERT INTO materials (
            material_id, material_type, strength_mpa,
            weight_capacity, biodegradability_percent,
            co2_emission_score, recyclability_percent,
            cost_per_kg, industry_use_case
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        tuple(row)
    )

conn.commit()
cur.close()
conn.close()

print("Materials ingested successfully")

