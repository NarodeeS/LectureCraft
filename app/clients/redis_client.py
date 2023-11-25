import redis.asyncio as redis

import config


redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
