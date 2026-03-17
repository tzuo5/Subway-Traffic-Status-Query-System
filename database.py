import psycopg2
from config import Config



class Database:
    def init_db(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="subway_db",
                user="subway_user",
                password="subway_user_password"
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

    def connect(self):
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="subway_db",
            user="subway_user",
            password="subway_user_password"
        )
        return conn

    def create_tables(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS subway_positions (
                id SERIAL PRIMARY KEY,
                trip_id VARCHAR(255) NOT NULL,
                route_id VARCHAR(255) NOT NULL,
                latitude DOUBLE PRECISION NOT NULL,
                longitude DOUBLE PRECISION NOT NULL,
                timestamp BIGINT NOT NULL
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

    def write_position(self, data):
        conn = self.connect()
        cur = conn.cursor()

        trip_id = data["trip_id"]
        route_id = data["route_id"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        timestamp = data["time_stamp"]

        cur.execute("""
            INSERT INTO subway_positions (trip_id, route_id, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s, %s);
        """, (trip_id, route_id, latitude, longitude, timestamp))

        conn.commit()
        cur.close()
        conn.close()

    def read_recent_positions(self, limit=100):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, trip_id, route_id, latitude, longitude, timestamp
            FROM subway_positions
            ORDER BY timestamp DESC
            LIMIT %s;
        """, (limit,))

        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "trip_id": row[1],
                "route_id": row[2],
                "latitude": row[3],
                "longitude": row[4],
                "timestamp": row[5]
            })

        cur.close()
        conn.close()

        print(result)
        return result


if __name__ == "__main__":
    db = Database()
    db.create_tables()
    print("success")