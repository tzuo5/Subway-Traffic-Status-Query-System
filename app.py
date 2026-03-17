from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import desc
import sys
import os

# Add project root directory to Python path to import config and utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from query_service.models import SessionLocal, SubwayPosition
from config import Config

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/subway/positions", methods=["GET"])
def get_all_subway_positions():
    db = SessionLocal()
    try:
        # For simplicity, fetch the latest 100 positions
        positions = db.query(SubwayPosition).order_by(desc(SubwayPosition.timestamp)).limit(100).all()
        results = []
        for pos in positions:
            results.append({
                "trip_id": pos.trip_id,
                "route_id": pos.route_id,
                "direction_id": pos.direction_id,
                "latitude": pos.latitude,
                "longitude": pos.longitude,
                "bearing": pos.bearing,
                "current_status": pos.current_status,
                "stop_id": pos.stop_id,
                "timestamp": pos.timestamp
            })
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/subway/positions/<route_id>", methods=["GET"])
def get_subway_positions_by_route(route_id):
    db = SessionLocal()
    try:
        # For simplicity, fetch the latest 50 positions for the given route
        positions = db.query(SubwayPosition).filter_by(route_id=route_id).order_by(desc(SubwayPosition.timestamp)).limit(50).all()
        results = []
        for pos in positions:
            results.append({
                "trip_id": pos.trip_id,
                "route_id": pos.route_id,
                "direction_id": pos.direction_id,
                "latitude": pos.latitude,
                "longitude": pos.longitude,
                "bearing": pos.bearing,
                "current_status": pos.current_status,
                "stop_id": pos.stop_id,
                "timestamp": pos.timestamp
            })
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.QUERY_API_PORT, debug=Config.FLASK_DEBUG)



