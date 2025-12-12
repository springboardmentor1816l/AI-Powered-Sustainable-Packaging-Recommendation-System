from fastapi import APIRouter
import psycopg2

router = APIRouter(prefix="/materials", tags=["Materials"])

DB_CONFIG = {
    "dbname": "ecopack_db",
    "user": "ecopack",
    "password": "ecopack123",
    "host": "db",
    "port": "5432"
}

@router.get("/")
def get_materials():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materials;")
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, r)) for r in rows]

    conn.close()
    return result
