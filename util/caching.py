from redis import Redis

from config import REDIS_URL


class Cache:
    """Used to store comment ids in cache.
    """

    redis = Redis.from_url(REDIS_URL)

    def redis_check(self, key):
        """Return `True` if `key` exist in redis DB.
        """
        if self.redis.exists(key):
            return True

    def redis_set(self, key, value):
        """Set ``key`` with ``value`` in redis DB.
        Key expires after 1 day (=24*60*60 seconds)
        """
        self.redis.set(name=key, value=value, ex=24 * 60 * 60)

    def check_comment(self, comment_id):
        """Check if comment is already processed/replied.
        Returns `True` if comment exists, else adds the comment to cache and returns `False`.
        """
        if self.redis_check(comment_id):
            return True
        else:
            self.redis_set(comment_id, "")
            return False
