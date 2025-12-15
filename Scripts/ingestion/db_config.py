import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="ecopack",
        user="postgres",
        password="2808",
        host="localhost",
        port=5432
    )
