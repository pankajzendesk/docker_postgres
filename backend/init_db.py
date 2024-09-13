import psycopg2
import os
import time

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')

# Retry logic
max_retries = 10
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                surname VARCHAR(100),
                age INTEGER
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized")
        break
    except psycopg2.OperationalError as e:
        print(f"Attempt {attempt+1}/{max_retries} failed: {e}")
        time.sleep(retry_delay)
else:
    raise Exception("Could not connect to the database after several retries")
