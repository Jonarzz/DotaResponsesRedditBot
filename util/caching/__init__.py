from config import CACHE_PROVIDER
from util.caching.db_cache import DBCache
from util.caching.memory_cache import MemoryCache
from util.caching.redis_cache import RedisCache


def get_cache_api():
    if CACHE_PROVIDER == 'redis':
        return RedisCache()
    elif CACHE_PROVIDER == 'memory':
        return MemoryCache()
    elif CACHE_PROVIDER == 'db':
        return DBCache()
