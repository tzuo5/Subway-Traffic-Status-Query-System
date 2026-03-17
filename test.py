import sys
import os
import time


STREAM_NAME = "subway:vehicle:position"
GROUP_NAME = "vehicle_group"
CONSUMER_NAME = "test_consumer"

sys.path.append(os.path.abspath("/Users/zuotianhao/Desktop/subway_project_simplified"))

from database import Database

database = Database()
database.init_db()

data = {
    "trip_id": 1,
    "route_id": 0,
    "time_stamp": 2,
    "latitude": 3,
    "longitude": 4
}

# database.write_position(data)


database.read_recent_positions()


