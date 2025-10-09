import redis.asyncio as aioredis
from src.config import REDIS_URL

redis_client = None

async def init_redis():
    global redis_client
    redis_client = await aioredis.from_url(
        "redis://redis:6379",
        encoding="utf-8",
        decode_responses=True
    )
    print("Redis initialized")

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        print("Redis connection closed")

def get_redis():
    if redis_client is None:
        raise RuntimeError("Redis not initialized yet")
    return redis_client