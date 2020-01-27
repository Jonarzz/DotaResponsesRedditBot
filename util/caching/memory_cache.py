"""Module used to save cache in the memory.
Uses FIFO eviction policy with maximum size of 10,000 and no ttl.
JSON File used to dump data on shutdown and load it back up on startup.
"""

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
        """Method that loads dumped cache from previous shutdown stored in json file.
        """
        self.cache = FIFOCache(maxsize=10_000, ttl=0, default='')
        if os.path.exists(CACHE_URL):
            with open(CACHE_URL) as cache_json:
                old_cache = json.load(cache_json, object_pairs_hook=OrderedDict)
                self.cache.set_many(old_cache)
        atexit.register(self._cleanup)

    def _cleanup(self):
        """Method to dump cache data to json file on script interrupt/shutdown.
        """
        with open(CACHE_URL, 'w+') as cache_json:
            json.dump(self.cache.copy(), cache_json)

    def _check(self, key):
        """Method to check if key exists in cache.

        :param key: The `key` to to be checked in cache.
        :return: `True` if `key` exist in cache.
        """
        return key in self.cache

    def _set(self, key):
        """Method to add thing_id to the cache.

        :param key: The `key` to be added to the cache.
        """
        self.cache.set(key, '')
