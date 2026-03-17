import redis

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        #print(self.client.ping())

    def add_to_stream(self, stream_name, data):
        return self.client.xadd(stream_name, data)

    def create_consumer_group(self, stream_name, group_name):
        print("=================================================================")
        print("creating consumer group")
        print("=================================================================")
        try:
            self.client.xgroup_create(
                stream_name,
                group_name,
                id="0",
                mkstream=True
            )
            print("Group created")
        except redis.exceptions.ResponseError:
            print("Group already exists")

    def read_from_stream(self, stream_name, group_name, consumer_name):
        messages = self.client.xreadgroup(
            groupname=group_name,
            consumername=consumer_name,
            streams={stream_name: ">"},
            count=1,
            block=2000
        )
        return messages



redis_client = RedisClient()
