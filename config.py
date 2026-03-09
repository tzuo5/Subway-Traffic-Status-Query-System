import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "subway_db")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

    QUERY_API_PORT = int(os.getenv("QUERY_API_PORT", "5000"))
    CONSUMER_SERVICE_PORT = int(os.getenv("CONSUMER_SERVICE_PORT", "5001"))

    MTA_API_URL = os.getenv(
        "MTA_API_URL",
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
    )
    FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", "30"))
