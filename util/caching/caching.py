"""Module used to store replyable ids (comment or submission) in cache.
Currently support only three implementations : DB based, in memory and redis.
Support for more implementations can be added by extending CacheAPI class.
"""

from abc import ABC, abstractmethod

__author__ = 'MePsyDuck'


class CacheAPI(ABC):
    @abstractmethod
    def _exists(self, key):
        pass

    @abstractmethod
    def _set(self, key):
        pass

    def exists(self, thing_id):
        """Check if Reddit thing (currently comment/submission) is already processed/replied.
        If it is not in the cache, it adds the thing_id to cache.

        :param thing_id: They id of comment/submission to be cached.
        :returns: `True` if replyable exists, else `False`.
        """
        if self._exists(thing_id):
            return True
        else:
            self._set(thing_id)
            return False
