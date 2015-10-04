# Dota Responses Reddit Bot
Bot adding reply comments with links to appropriate responses found on /r/dota2.

![Example](http://i.imgur.com/loqqDXk.png)

The bot replies only for the comments that **are** responses ~~or for the comments starting with hero name and having the response after a colon~~ (TODO). 

For example:
"Ho ho ha ha" will return an Axe response, ~~but "Sniper: ho ho ha ha" will return a Sniper response~~. 
All the responses are in lowercase in the dictionary, before comparision the comments are parsed to lowercase as well. Dot or exclamation mark ending the comment is ignored.

---
# Changelog:
#####1.1:
* one word responses are no longer in the dictionary
* replaced double spaces with single space
* bot is now working with hot submissions

#####1.2:
* accept comments with extra letters added for emphasis

---
# TODO:
* add dictionaries for all heroes (see example with colon)
* keywords that trigger the bot
* remove responses such as "thank you" and item names (anti-spam)

