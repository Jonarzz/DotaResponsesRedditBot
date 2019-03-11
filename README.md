# Dota Responses Reddit Bot
[![Build Status](https://travis-ci.com/MePsyDuck/DotaResponsesRedditBot.svg?branch=master)](https://travis-ci.com/MePsyDuck/DotaResponsesRedditBot)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/96e2b3fd0dfd495f87fda7dfad5fb545)](https://app.codacy.com/app/MePsyDuck/DotaResponsesRedditBot?utm_source=github.com&utm_medium=referral&utm_content=MePsyDuck/DotaResponsesRedditBot&utm_campaign=Badge_Grade_Dashboard)
[![codecov](https://codecov.io/gh/MePsyDuck/DotaResponsesRedditBot/branch/master/graph/badge.svg)](https://codecov.io/gh/MePsyDuck/DotaResponsesRedditBot)


Bot adding reply comments with links to appropriate responses found on [/r/dota2](https://www.reddit.com/r/DotA2).

![Example](https://i.imgur.com/PAcg57z.png)

The bot replies only for the comments that **are** responses. 

For example: `"Selemene commands"` will return a Luna response *(like on the screenshot above)*. 

All the responses are in lowercase in the dictionary, before comparision the comments are parsed to lowercase as well. Dot or exclamation mark ending the comment is ignored.

The bot will try to match a response of the hero that is in the comment's author flair. If it does not find an appropriate one, it takes the one of the first hero that has such a response (alphabetically).


---
## TODO:
Target: to complete the following in March
* ~~Make the bot work in r/test~~ _(Rejoice! It works!!!)_
* Add support for flair in responses
* Improve tests
* Refactor code
* Docs
* Add support for custom responses
* Change the comment footer to universal (old, new and mobile reddit) format.
* Use redis(or any other in-memory storage) for comment id caching

---
## Changelog:

##### 2.7:
* Now hero portraits (flairs) are added before the response
* The bot tries to match the hero response with the hero in the comment's author flair first

##### 2.6:
* Added a few Io and Phoenix responses

##### 2.5:
* Fixed random responses for the "Shitty wizard" line - now it's working properly
* Added special treatment for the comments related to "One of my favorites" response
* Moved from a dictionary for responses and a list for comment ids to databases

##### 2.4:
* Added random responses for the "Shitty wizard" line (needs testing)

##### 2.3:
* Added tests
* Code refactoring
* Added Travis CI and CodeClimate checking

##### 2.2:
* Code refactoring (renaming variables, deleting unnecessary methods, etc.)
* Response in the reply is now an exact quote of the original comment
* Added comments

##### 2.1:
* Bot is now adding the source of the response (e.g. hero name) to the comment *(needs testing)*

##### 2.0:
* Added Arc Warden responses

##### 1.9:
* File paths are now relative to the script file location (using os)
* Added dates to logging
* Logs are saved in respective files on the server
* Fixed a bug with adding same comment a few times in sticky threads that are on the subreddit for a long time (time-saving workaround)

##### 1.8:
* Change in the main loop of the script - much better efficiency (time)

##### 1.7:
* Changed reply comment formatting

##### 1.6:
* Removed keyword triggering as /r/dota2 community did not like it

##### 1.5:
* Added keywords that trigger the bot: "just do it", "beautiful", "from the ghastly eyrie", "sniper", "ppd", "leafeator", "ur/your brother"
* Code refactoring

##### 1.4:
* Fixed a bug created by 1.2 changes
* Changed submissions number in hot to 25
* Added more excluded responses

##### 1.3:
* Removed responses such as "thank you", hero names and item names (anti-spam)

##### 1.2:
* Accept comments with extra letters added for emphasis

##### 1.1:
* One word responses are no longer in the dictionary
* Replaced double spaces with single space
* Bot is now working with hot submissions

---
### Treeware License
Basically MIT License, but if you use the code (learning or project purposes), you have to plant at least one tree at some future time.
