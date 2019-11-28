"""Module used to store thing ids (comment or submission) in cache.
Currently support only three implementations : DB based, in memory and redis.
Support for more implementations can be added by extending CacheAPI class.
"""

from abc import ABC, abstractmethod

__author__ = 'MePsyDuck'


class CacheAPI(ABC):
    @abstractmethod
    def _check(self, thing_id):
        pass

    @abstractmethod
    def _set(self, thing_id):
        pass

    def check(self, thing_id):
        """Check if thing or submission is already processed/replied.
        If it is not in the cache, it adds the thing_id to cache.

        :param thing_id: They id of comment/submission to be cached.
        :returns: `True` if thing exists, else `False`.
        """
        if self._check(thing_id):
            return True
        else:
            self._set(thing_id)
            return False
