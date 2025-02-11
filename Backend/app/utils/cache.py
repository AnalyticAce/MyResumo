import json
import redis
from typing import Dict, Optional
from app import REDIS_HOST, REDIS_PORT

class CacheManager:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=REDIS_HOST,
            port=int(REDIS_PORT),
            decode_responses=True,
        )

    async def get_cached(self, namespace: str, key: str) -> Optional[Dict]:
        cache_key = f"{namespace}:{key}"
        cached_data = self.redis_client.get(cache_key)
        return json.loads(cached_data) if cached_data else None
        
    async def update_cache(self, namespace: str, key: str, data: Dict) -> Dict:
        cache_key = f"{namespace}:{key}"
        self.redis_client.set(cache_key, json.dumps(data))
        return data