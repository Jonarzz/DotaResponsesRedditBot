# Dota Responses Reddit Bot
[![Build Status](https://travis-ci.org/Jonarzz/DotaResponsesRedditBot.svg?branch=master)](https://travis-ci.org/Jonarzz/DotaResponsesRedditBot) [![Code Climate](https://codeclimate.com/github/Jonarzz/DotaResponsesRedditBot/badges/gpa.svg)](https://codeclimate.com/github/Jonarzz/DotaResponsesRedditBot) [![Issue Count](https://codeclimate.com/github/Jonarzz/DotaResponsesRedditBot/badges/issue_count.svg)](https://codeclimate.com/github/Jonarzz/DotaResponsesRedditBot)

Bot adding reply comments with links to appropriate responses found on /r/dota2.

*Thanks to /u/iggys_reddit_account the bot is running 24/7.*

![Example](http://i.imgur.com/wOIbrTY.png)

The bot replies only for the comments that **are** responses. 

For example:
"Selemene commands" will return a Luna response (like on the screenshot above). 

All the responses are in lowercase in the dictionary, before comparision the comments are parsed to lowercase as well. Dot or exclamation mark ending the comment is ignored.

---
# Changelog:
#####2.3:
* added tests
* code refactoring
* added Travis CI and CodeClimate checking

#####2.2:
* code refactoring (renaming variables, deleting unnecessary methods, etc.)
* response in the reply is now an exact quote of the original comment
* added comments

#####2.1:
* bot is now adding the source of the response (e.g. hero name) to the comment *(needs testing)*

#####2.0:
* added Arc Warden responses

#####1.9:
* file paths are now relative to the script file location (using os)
* added dates to logging
* logs are saved in respective files on the server
* fixed a bug with adding same comment a few times in sticky threads that are on the subreddit for a long time (time-saving workaround)

#####1.8:
* change in the main loop of the script - much better efficiency (time)

#####1.7:
* changed reply comment formatting

#####1.6:
* removed keyword triggering as /r/dota2 community did not like it

#####1.5:
* added keywords that trigger the bot: "just do it", "beautiful", "from the ghastly eyrie", "sniper", "ppd", "leafeator", "ur/your brother"
* code refactoring

#####1.4:
* fixed a bug created by 1.2 changes
* changed submissions number in hot to 25
* added more excluded responses

#####1.3:
* removed responses such as "thank you", hero names and item names (anti-spam)

#####1.2:
* accept comments with extra letters added for emphasis

#####1.1:
* one word responses are no longer in the dictionary
* replaced double spaces with single space
* bot is now working with hot submissions

---
# Further plans:
* start with tests the next time (TDD)
* fix CodeClimate issues
