import redis

def get_redis_connection():
    return redis.Redis(
        host="redis",
        port=6379,
        db=0,
        decode_responses=True
    )