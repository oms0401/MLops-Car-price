import json
import redis
from app.core.config import setting

redis_client = redis.Redis.from_url(setting.REDIS_URL)

def get_cached_prediction(key : str):
    value = redis_client.get(key)
    if value:
        return json.load(value)
    return None

def set_cached_prediction(key: str, value: dict, expiry: int = 3600):
    redis_client.setex(key, expiry, value=json.dumps(value))