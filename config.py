"""Module in which the constants that are used by Dota Responses Bot are declared."""
import os

__author__ = 'Jonarzz'
__maintainer__ = 'MePsyDuck'

# App config
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
EXCEPTION_TIMEOUT = 120
USER_AGENT = 'Python:dota2_responses_bot:v3.1 by /u/Jonarzz, maintained by /u/MePsyDuck'

# Caching config
CACHE_PROVIDER = os.environ.get('CACHE_PROVIDER', 'memory')  # valid choices : redis, memory, db
CACHE_URL = os.environ.get('CACHE_URL',
                           os.path.join(os.getcwd(), 'cache.json'))  # file path in case of memory/file based caching

# DB config
DB_PROVIDER = os.environ.get('DATABASE_PROVIDER', 'sqlite')  # valid choices : sqlite, mysql, postgres
DB_URL = os.environ.get('DATABASE_URL', os.path.join(os.getcwd(), 'bot.db'))  # file path in case of sqlite

# Logging config
BOT_LOGGER = 'bot'
PRAW_LOGGER = 'prawcore'
LOG_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(funcName)-25s %(message)s'
LOG_DIR = 'logs'
INFO_FILENAME = 'info.log'
WARN_FILENAME = 'warn.log'
ERROR_FILENAME = 'error.log'
PRAW_FILENAME = 'praw.log'

CACHE_TTL = 5
