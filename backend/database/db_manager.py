import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict
import os
import time

# backend/database/db_manager.py
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict
import os
import time

class DBManager:
    def __init__(self, max_retries=5, retry_delay=5):
        self.conn = None
        self.connect_with_retry(max_retries, retry_delay)

    def connect_with_retry(self, max_retries, retry_delay):
        for attempt in range(max_retries):
            try:
                self.conn = psycopg2.connect(
                    dbname=os.getenv('POSTGRES_DB', 'sentiment_db'),
                    user=os.getenv('POSTGRES_USER', 'user'),
                    password=os.getenv('POSTGRES_PASSWORD', 'password'),
                    host=os.getenv('DB_HOST', 'db'),
                    port=os.getenv('DB_PORT', '5432')
                )
                print(f"Successfully connected to the database on attempt {attempt + 1}")
                return
            except psycopg2.OperationalError as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Could not connect to the database.")
                    raise e

    def store_raw_data(self, data: List[Dict]):
        with self.conn.cursor() as cur:
            for item in data:
                cur.execute(
                    "INSERT INTO raw_data (id, text, created_at, user_name) VALUES (%s, %s, %s, %s)",
                    (item['id'], item['text'], item['created_at'], item['user'])
                )
        self.conn.commit()

    def get_raw_data(self) -> List[Dict]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM raw_data")
            return cur.fetchall()

    def store_cleaned_data(self, data: List[Dict]):
        with self.conn.cursor() as cur:
            for item in data:
                cur.execute(
                    "INSERT INTO cleaned_data (id, cleaned_text, created_at, user_name) VALUES (%s, %s, %s, %s)",
                    (item['id'], item['cleaned_text'], item['created_at'], item['user'])
                )
        self.conn.commit()

    def get_cleaned_data(self) -> List[Dict]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM cleaned_data")
            return cur.fetchall()

    def store_analyzed_data(self, data: List[Dict]):
        with self.conn.cursor() as cur:
            for item in data:
                cur.execute(
                    "INSERT INTO analyzed_data (id, sentiment, score, created_at, user_name) VALUES (%s, %s, %s, %s, %s)",
                    (item['id'], item['sentiment'], item['score'], item['created_at'], item['user'])
                )
        self.conn.commit()

    def get_analyzed_data(self) -> List[Dict]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM analyzed_data")
            return cur.fetchall()