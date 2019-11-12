from abc import ABC, abstractmethod

from config import CACHE_PROVIDER
from util.caching.in_memory_cache import MemoryCache
from util.caching.redis_cache import RedisCache

__author__ = 'MePsyDuck'


class CacheAPI(ABC):
    """Used to store comment ids in cache_api.
    Currently support only three implementations : DB based, in memory, file based and redis.
    Support for more implementations can be added by extending this class.
    """

    @abstractmethod
    def check(self, comment_id):
        pass

    @abstractmethod
    def set(self, comment_id):
        pass

    def check_comment(self, comment_id):
        """Check if comment is already processed/replied.
        Returns `True` if comment exists, else adds the comment to cache_api and returns `False`.
        """
        if self.check(comment_id):
            return True
        else:
            self.set(comment_id)
            return False


def get_cache_api():
    if CACHE_PROVIDER == 'redis':
        return RedisCache()
    elif CACHE_PROVIDER == 'memory':
        return MemoryCache()
    elif CACHE_PROVIDER == 'file':
        return MemoryCache()  # TODO impl
    elif CACHE_PROVIDER == 'db':
        return MemoryCache()  # TODO impl
