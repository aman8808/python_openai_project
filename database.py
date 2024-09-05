import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from config import DATABASE_CONFIG

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    register_vector(conn)
    return conn

def create_vector(vector_data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO vectors (vector, metadata) VALUES (%s, %s) RETURNING id;",
                (vector_data['vector'], vector_data['metadata'])
            )
            conn.commit()
            vector_id = cursor.fetchone()[0]
    finally:
        conn.close()
    return vector_id

def get_vectors():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM vectors;")
            vectors = cursor.fetchall()
    finally:
        conn.close()
    return vectors

def create_query(query_text):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO queries (query) VALUES (%s) RETURNING id;",
                (query_text,)
            )
            conn.commit()
            query_id = cursor.fetchone()[0]
    finally:
        conn.close()
    return query_id

def create_response(query_id, response_text):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO responses (query_id, response) VALUES (%s, %s);",
                (query_id, response_text)
            )
            conn.commit()
    finally:
        conn.close()
