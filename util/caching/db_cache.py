from util.caching.caching import CacheAPI
from util.database.database import db_api

__author__ = 'MePsyDuck'


class DBCache(CacheAPI):
    def check(self, key):
        """Return `True` if `key` exist in cache_list.
        """
        return db_api.check_if_comment_exists(key)

    def set(self, key):
        """Add comment_id to the cache_list
        """
        db_api.add_comment_to_table(key)
