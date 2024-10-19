import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'querymanager',
    'user': 'postgres',
    'password': 'pgadmin1234',
    'host': 'localhost',
    'port': '5432'
}

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=None, fetch=False):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
        conn.commit()
