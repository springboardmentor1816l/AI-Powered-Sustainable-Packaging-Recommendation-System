import pandas as pd
from db_config import get_connection

df = pd.read_csv("data/processed(1)/products_updated.csv")

conn = get_connection()
cur = conn.cursor()

# 🔥 Clear existing data (important)
cur.execute("TRUNCATE TABLE products RESTART IDENTITY CASCADE;")

for _, row in df.iterrows():
    cur.execute(
        """
        INSERT INTO products (
            product_id, product_name, category,
            product_weight, fragility_index, shipping_type
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        tuple(row)
    )

conn.commit()
cur.close()
conn.close()

print("Products ingested successfully")

