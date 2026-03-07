import os
import psycopg2

# load database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres-db"),
    "database": os.getenv("DB_NAME", "ecommerce_db"),
    "user": os.getenv("DB_USER", "ecommerceuser"),
    "password": os.getenv("DB_PASSWORD", "ecadminpass"),
    "port": 5432,
}


def get_db_connection():
    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    return connection


def read_from_db(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def write_to_db(query, params=None):
    conn = get_db_connection
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
