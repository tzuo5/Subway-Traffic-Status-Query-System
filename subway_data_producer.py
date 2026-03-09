from google.transit import gtfs_realtime_pb2
import requests
import redis_client
import time

STREAM_NAME = "subway:vehicle:position"
GROUP_NAME = "vehicle_group"
CONSUMER_NAME = "test_consumer"


def fetch_and_produce_data(api, client):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(api)
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            #提取
            trip_id = entity.vehicle.trip.trip_id
            route_id = entity.vehicle.trip.route_id
            time_stamp = entity.vehicle.timestamp
            if (entity.vehicle.position.HasField('latitude')):
                latitude = entity.vehicle.position.latitude
            else:
                latitude = 0.0


            if (entity.vehicle.position.HasField('longitude')):
                longitude = entity.vehicle.position.longitude
            else:
                longitude = 0.0

            #转换
            data = {
                "trip_id": trip_id,
                "route_id": route_id,
                "time_stamp": time_stamp,
                "latitude": latitude,
                "longitude": longitude
            }
            client.add_to_stream(STREAM_NAME, data)
    #print("success")
        


def consume(client):
    messages = client.read_from_stream(
        STREAM_NAME,
        GROUP_NAME,
        CONSUMER_NAME
    )

    print("Read:", messages)

#====================================================================================================================================================================================================================================================================
#====================================================================================================================================================================================================================================================================

if __name__ == "__main__":

    api = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"

    client = redis_client.RedisClient()

    client.create_consumer_group(STREAM_NAME, GROUP_NAME)

    while True:
        fetch_and_produce_data(api, client)
        print(idx)
        print(consume(client))
        time.sleep(60)