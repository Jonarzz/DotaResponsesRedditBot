from redis import Redis

from config import CACHE_URL, CACHE_TTL
from util.caching.caching import CacheAPI
from util.logger import logger

__author__ = 'MePsyDuck'


class RedisCache(CacheAPI):
    def __init__(self):
        """Create a new Redis instance when a new object for this class is created.
        """
        self.redis = Redis.from_url(CACHE_URL)
        logger.info('Connected to Redis at ' + CACHE_URL)

    def _check(self, key):
        """Return `True` if `key` exist in redis DB.
        """
        if self.redis.exists(key):
            return True

    def _set(self, key):
        """Set ``key`` with ``value`` in redis DB.
        Key expires after 1 day (=24*60*60 seconds)
        """
        self.redis.set(name=key, value='', ex=CACHE_TTL * 60 * 60)
