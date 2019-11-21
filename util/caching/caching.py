from abc import ABC, abstractmethod

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


