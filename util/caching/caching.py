from abc import ABC, abstractmethod

__author__ = 'MePsyDuck'


class CacheAPI(ABC):
    """Used to store thing ids (thing or submission) in cache_api.
    Currently support only three implementations : DB based, in memory, file based and redis.
    Support for more implementations can be added by extending this class.
    """

    @abstractmethod
    def _check(self, thing_id):
        pass

    @abstractmethod
    def _set(self, thing_id):
        pass

    def check(self, thing_id):
        """Check if thing or submission is already processed/replied.
        Returns `True` if thing exists, else adds the thing to cache_api and returns `False`.
        """
        if self._check(thing_id):
            return True
        else:
            self._set(thing_id)
            return False


