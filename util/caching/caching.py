from config import REDIS_URL
from util.logger import logger

__author__ = 'MePsyDuck'


class Cache:
    """Used to store comment ids in cache.
    """

    redis = None

    def __init__(self):
        """Create a new Redis instance when a new object for this class is created.
        """
        self.redis = []
        # self.redis = Redis.from_url(REDIS_URL)
        logger.info('Connected to Redis at ' + REDIS_URL)

    def __del__(self):
        """This method is not actually needed since Redis automatically handles connections, but added it anyway to
        dereference the connection variable.
        """
        self.redis = None
        # logger.info('Closed connection to Redis at ' + REDIS_URL)

    def redis_check(self, key):
        """Return `True` if `key` exist in redis DB.
        """
        # if self.redis.exists(key):
        if key in self.redis:
            return True

    def redis_set(self, key, value):
        """Set ``key`` with ``value`` in redis DB.
        Key expires after 1 day (=24*60*60 seconds)
        """
        # self.redis.set(name=key, value=value, ex=24 * 60 * 60)
        self.redis.append(key)

    def check_comment(self, comment_id):
        """Check if comment is already processed/replied.
        Returns `True` if comment exists, else adds the comment to cache and returns `False`.
        """
        if self.redis_check(comment_id):
            return True
        else:
            self.redis_set(comment_id, "")
            return False
