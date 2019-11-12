from util.caching.caching import CacheAPI

__author__ = 'MePsyDuck'


class MemoryCache(CacheAPI):
    def __init__(self):
        self.cache_list = []

    def redis_check(self, key):
        """Return `True` if `key` exist in cache_list.
        """
        if key in self.cache_list:
            return True

    def redis_set(self, key):
        """Add comment_id to the cache_list
        """
        self.cache_list.append(key)
