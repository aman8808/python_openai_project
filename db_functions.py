import psycopg2
import numpy as np
import ast
from config import DATABASE_CONFIG

def get_vectors():
    conn = psycopg2.connect(DATABASE_CONFIG['url'])
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, vector FROM vectors")
        vectors_data = cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        vectors_data = []
    finally:
        cursor.close()
        conn.close()

    vectors_data = [(id, np.array(ast.literal_eval(vector), dtype=np.float32)) for id, vector in vectors_data]
    return vectors_data

def insert_vector(id, vector):
    conn = psycopg2.connect(DATABASE_CONFIG['url'])
    cursor = conn.cursor()

    try:
        vector_str = vector.tolist()  # Преобразование вектора в список
        cursor.execute("""
            INSERT INTO vectors (id, vector)
            VALUES (%s, %s)
            ON CONFLICT (id) 
            DO UPDATE SET vector = EXCLUDED.vector
        """, (id, vector_str))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке/обновлении данных: {e}")
    finally:
        cursor.close()
        conn.close()

def delete_vector(id):
    conn = psycopg2.connect(DATABASE_CONFIG['url'])
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM vectors WHERE id = %s", (id,))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении данных: {e}")
    finally:
        cursor.close()
        conn.close()

def create_query(query_text):
    conn = psycopg2.connect(DATABASE_CONFIG['url'])
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO queries (query)
            VALUES (%s) RETURNING id
        """, (query_text,))
        query_id = cursor.fetchone()[0]
        conn.commit()
    except Exception as e:
        print(f"Ошибка при создании запроса: {e}")
        query_id = None
    finally:
        cursor.close()
        conn.close()

    return query_id

def create_response(query_id, response_text, tokens_used):
    conn = psycopg2.connect(DATABASE_CONFIG['url'])
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO responses (query_id, response, tokens_used)
            VALUES (%s, %s, %s)
        """, (query_id, response_text, tokens_used))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при создании ответа: {e}")
    finally:
        cursor.close()
        conn.close()
