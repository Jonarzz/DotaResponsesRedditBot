from util.caching.caching import CacheAPI
from util.database.database import db_api

__author__ = 'MePsyDuck'


class DBCache(CacheAPI):
    """Needs manual clearing of old ids.
    """

    def _check(self, key):
        """Return `True` if `key` exist in cache_list.
        """
        return db_api.check_if_thing_exists(key)

    def _set(self, key):
        """Add comment_id to the cache_list
        """
        db_api.add_thing_to_cache(key)
