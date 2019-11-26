import atexit
import json
import os
from collections import OrderedDict

from cacheout import FIFOCache

from config import CACHE_URL
from util.caching.caching import CacheAPI

__author__ = 'MePsyDuck'


class MemoryCache(CacheAPI):
    def __init__(self):
        self.cache = FIFOCache(maxsize=10_000, ttl=0, default='')
        if os.path.exists(CACHE_URL):
            with open(CACHE_URL) as cache_json:
                old_cache = json.load(cache_json, object_pairs_hook=OrderedDict)
                self.cache.set_many(old_cache)
        atexit.register(self._cleanup)

    def _cleanup(self):
        with open(CACHE_URL, 'w+') as cache_json:
            json.dump(self.cache.copy(), cache_json)

    def _check(self, key):
        """Return `True` if `key` exist in cache_list.
        """
        return key in self.cache

    def _set(self, key):
        """Add comment_id to the cache_list
        """
        self.cache.set(key, '')
