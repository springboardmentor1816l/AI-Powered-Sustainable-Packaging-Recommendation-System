from db_config import get_connection

try:
    conn = get_connection()
    print("DB connection successful")
    conn.close()
except Exception as e:
    print("DB connection failed:", e)
