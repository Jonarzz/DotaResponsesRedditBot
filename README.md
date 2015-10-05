# Dota Responses Reddit Bot
Bot adding reply comments with links to appropriate responses found on /r/dota2.

![Example](http://i.imgur.com/loqqDXk.png)

The bot replies only for the comments that **are** responses. 

For example:
"Selemene commands" will return a Luna response (like on the screenshot above). 
All the responses are in lowercase in the dictionary, before comparision the comments are parsed to lowercase as well. Dot or exclamation mark ending the comment is ignored.

---
# Changelog:
#####1.1:
* one word responses are no longer in the dictionary
* replaced double spaces with single space
* bot is now working with hot submissions

#####1.2:
* accept comments with extra letters added for emphasis

#####1.3:
* removed responses such as "thank you", hero names and item names (anti-spam)

#####1.4:
* fixed a bug created by 1.2 changes
* changed submissions number in hot to 25
* added more excluded responses

---
# TODO:
* add dictionaries for all heroes (if needed)
* keywords that trigger the bot


