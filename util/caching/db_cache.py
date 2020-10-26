"""Module to store thing_ids in DB.
Not recommended as this needs manual clearing of old ids.
"""

from util.caching.caching import CacheAPI
from util.database.database import db_api

__author__ = 'MePsyDuck'


class DBCache(CacheAPI):
    def _exists(self, key):
        """Method to check if key exists in DB cache.

        :param key: The `key` to to be checked in DB cache.
        :return: `True` if `key` exist in DB cache.
        """
        return db_api.check_if_thing_exists(key)

    def _set(self, key):
        """Method to set `key` with `value` in DB cache.

        :param key: The `key` (thing_id) to be added to DB cache.
        """
        db_api.add_thing_to_cache(key)
