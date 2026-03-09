import psycopg2
import sys
import os

# Add parent directory to Python path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

def init_db():
    conn = None
    try:
        conn = psycopg2.connect(
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS subway_positions (
                id SERIAL PRIMARY KEY,
                trip_id VARCHAR(255) NOT NULL,
                route_id VARCHAR(255) NOT NULL,
                direction_id INTEGER,
                latitude DOUBLE PRECISION NOT NULL,
                longitude DOUBLE PRECISION NOT NULL,
                bearing INTEGER,
                current_status VARCHAR(50),
                stop_id VARCHAR(255),
                timestamp BIGINT NOT NULL
            );
        """)
        conn.commit()
        print("Database and table created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()


