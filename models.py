from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

# Add project root directory to Python path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

DATABASE_URL = f"postgresql://postgres:subway_pass@localhost/postgres"

Base = declarative_base()

class SubwayPosition(Base):
    __tablename__ = "subway_positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String, nullable=False)
    route_id = Column(String, nullable=False)
    direction_id = Column(Integer)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    bearing = Column(Integer)
    current_status = Column(String)
    stop_id = Column(String)
    timestamp = Column(BigInteger, nullable=False)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



