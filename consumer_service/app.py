import sys
import os
import time
import string

STREAM_NAME = "subway:vehicle:position"
GROUP_NAME = "vehicle_group"
CONSUMER_NAME = "test_consumer"

sys.path.append(os.path.abspath("/Users/zuotianhao/Desktop/subway_project_simplified"))

from redis_client import redis_client
from database import Database

database = Database()
database.init_db()



def consume(client):
    print("#################################" + str(running))
    while running:
        messages = client.read_from_stream(
            STREAM_NAME,
            GROUP_NAME,
            CONSUMER_NAME
        )
        print("message: " + str(messages))
        # if not messages:
        #     time.sleep(1)
        # else:
        print("Read:", str(messages)) #----> 加入逻辑，将messages加入postgreSQL 数据库
        

# while True:
#     consume(redis_client)
#     time.sleep(1)


running = True

from flask import Flask, jsonify, request

app = Flask(__name__)

# -----------------------
# Config
# -----------------------
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False

# -----------------------
# Health Check
# -----------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200

# -----------------------
# Start
# -----------------------
@app.route("/start", methods=["POST"])
def start_consumer():
    data = {
        "message": "Flask API running"
    }
    running = True
    print("executed")
    consume(redis_client)
    return jsonify({
         "message": "consumer running"
    }), 200

# -----------------------
# POST Example
# -----------------------
@app.route("/stop", methods=["POST"])
def stop_consumer():
    running = False
    return jsonify({
         "message": "consumer stops running"
    }), 200




# -----------------------
# Run Server
# -----------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5555
    )

    