"""Module that allows Redis to be used as cache. Useful when running on Heroku or such platforms without persistent
file storage.
"""

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
        """Method to check if `key` exists in redis cache.

        :param key: The `key` to to be checked in redis cache.
        :return: `True` if `key` exists in redis cache.
        """
        if self.redis.exists(key):
            return True

    def _set(self, key):
        """Method to set `key` with `value` in redis.
        Key expires after CACHE_TTL days (`ex` in seconds).

        :param key: The `key` (thing_id) to be added to redis cache.
        """
        self.redis.set(name=key, value='', ex=CACHE_TTL * 60 * 60)
