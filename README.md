## Dota Responses Reddit Bot
[![Python 3.8.5](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-364/)
[![Build Status](https://api.travis-ci.org/Jonarzz/DotaResponsesRedditBot.svg?branch=master)](https://travis-ci.org/Jonarzz/DotaResponsesRedditBot)
[![Maintainability](https://api.codeclimate.com/v1/badges/de2c724018076b34064f/maintainability)](https://codeclimate.com/github/Jonarzz/DotaResponsesRedditBot/maintainability)
[![codecov](https://codecov.io/gh/Jonarzz/DotaResponsesRedditBot/branch/master/graph/badge.svg)](https://codecov.io/gh/Jonarzz/DotaResponsesRedditBot)

> Bot adding reply comments with links to appropriate responses found on [/r/dota2](https://www.reddit.com/r/DotA2).

![Example](https://i.imgur.com/PAcg57z.png)

The bot replies only for the comments that **are** responses. 

For example: `"Selemene commands"` will return a Luna response *(like on the screenshot above)*. 

### Active maintainer
[MePsyDuck](https://github.com/MePsyDuck)

### Comment/Submission text processing
*   All the body text is transformed into lowercase
*   Any punctuation is replaced with spaces
*   Multiple spaces are trimmed to single space.
*   If comment has blockquote, first blockquote is considered for matching.

<!-- Old behavior
All the responses are in lowercase in the dictionary, before comparison the comments are parsed to lowercase as well. Dot or exclamation mark ending the replyable is ignored.
-->
<!-- Old behavior
The bot will try to match a response of the hero that is in the comment/submission's author flair. If it does not find an appropriate one, it takes the one of the first hero that has such a response (alphabetically).
-->

---
### TODO
*   (If possible) Add hero flair in responses (Waiting on reddit to support this in reddit redesign).
*   Log query stats on shutdown
*   Log bot usage stats in DB
*   Make config excluded responses to be populated on startup 
*   Add new command to show usage stats
*   Add more test cases
*   Add Io, Phoenix, Marci Dota Plus Chat Wheel lines

---
### Some stats and general info
[/r/dota2](https://www.reddit.com/r/DotA2) subreddit generates around 3.5k comments/day, 
peaking around 12.5k during December (stats via [subbreditstats](https://subredditstats.com/r/dota2). 
Bot should be able to handle more than 15k comments/day(10 comments/minute) easily (Just an estimate, actual performance not yet tested).

---
### Environment variables 
Config variables needed to be set in environment for running the bot:

|     Variable      | Required? |   Default    | Description                                                                                            |
|-------------------|-----------|--------------|--------------------------------------------------------------------------------------------------------|
| CLIENT_ID         | Required  | None.        | `client_id` generated by Reddit.                                                                       |
| CLIENT_SECRET     | Required  | None.        | `secret` generated by Reddit.                                                                          |
| SUBREDDIT         | Optional  | `dota2`      | Subreddit the bot is going to work on.                                                                 |
| REDDIT_USERNAME   | Required  | None.        | Username for the Reddit account being used.                                                            |
| REDDIT_PASSWORD   | Required  | None.        | Password for the Reddit account being used.                                                            |
| CACHE_PROVIDER    | Optional  | `memory`     | Caching module to be used. Valid choices : `redis`, `memory`, `db`.                                    |
| CACHE_URL         | Optional  | `cache.json` | URL path to redis instance/database/file in memory. Based on `CACHE_PROVIDER`.                         |
| DATABASE_PROVIDER | Optional  | `sqlite`     | DBMS to be used. Valid choices : `sqlite`, `mysql`, `postgres`                                         |
| DATABASE_URL      | Optional  | `bot.db`     | URL to the database.                                                                                   |
| LOGGING_LEVEL     | Optional  | `INFO`       | Logging level. Valid choices : [Logging levels](https://docs.python.org/3/library/logging.html#levels) |

---
### Changelog
#### 3.2
*   Formatting fixes for comments.
*   Added supported club voice lines.
*   Added TI Talent voice lines.

#### 3.1
*   User(OP) can now request to update the response using another comment under bot's comment.
    The comment should be in the format ```Try <hero_name>``` 
*   Users can now request for a hero specific response by adding ```<hero_name> ::``` prefix to the response.
    Has more priority than user's flair.

#### 3.0
Major revamp for the bot.
Things that are new:
*   Bot can reply to responses that are in blockquotes and ignore rest of comment.
*   Added support for TI chat wheel sounds.
*   Comment on post submission if title is a response.

Things updated:
*   Support sqlite, MySQL and PostgreSQL dbs via Pony-ORM.
*   Added caching for comment ids (redis, db and in memory/file based).
*   Revamped parsing of responses from wiki (now directly from the sources).
*   Revamped parsing flair css and image directories from subreddit css.
*   Better parsing for comments.
*   Added better support for custom responses.
*   Updated excluded responses.
*   Updated docs.
*   Updated tests. 

#### 2.7
*   Now hero portraits (flairs) are added before the response
*   The bot tries to match the hero response with the hero in the comment's author flair first

#### 2.6
*   Added a few Io and Phoenix responses

#### 2.5
*   Fixed random responses for the "Shitty wizard" line - now it's working properly
*   Added special treatment for the comments related to "One of my favorites" response
*   Moved from a dictionary for responses and a list for comment ids to databases

#### 2.4
*   Added random responses for the "Shitty wizard" line (needs testing)

#### 2.3
*   Added tests
*   Code refactoring
*   Added Travis CI and CodeClimate checking

#### 2.2
*   Code refactoring (renaming variables, deleting unnecessary methods, etc.)
*   Response in the reply is now an exact quote of the original comment
*   Added comments

#### 2.1
*   Bot is now adding the source of the response (e.g. hero name) to the comment *(needs testing)*

#### 2.0
*   Added Arc Warden responses

#### 1.9
*   File paths are now relative to the script file location (using os)
*   Added dates to logging
*   Logs are saved in respective files on the server
*   Fixed a bug with adding same comment a few times in sticky threads that are on the subreddit for a long time (time-saving workaround)

#### 1.8
*   Change in the main loop of the script - much better efficiency (time)

#### 1.7
*   Changed reply comment formatting

#### 1.6
*   Removed keyword triggering as /r/dota2 community did not like it

#### 1.5
*   Added keywords that trigger the bot: "just do it", "beautiful", "from the ghastly eyrie", "sniper", "ppd", "leafeator", "ur/your brother"
*   Code refactoring

#### 1.4
*   Fixed a bug created by 1.2 changes
*   Changed submissions number in hot to 25
*   Added more excluded responses

#### 1.3
*   Removed responses such as "thank you", hero names and item names (anti-spam)

#### 1.2
*   Accept comments with extra letters added for emphasis

#### 1.1
*   One word responses are no longer in the dictionary
*   Replaced double spaces with single space
*   Bot is now working with hot submissions

---
### Treeware License
Basically MIT License, but if you use the code (learning or project purposes), you have to plant at least one tree at some future time.
