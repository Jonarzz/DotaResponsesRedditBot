# Dota Responses Reddit Bot
Bot adding reply comments with links to appropriate responses found on /r/dota2.

![Example](http://i.imgur.com/loqqDXk.png)

The bot replies only for the comments that **are** responses. 

For example:
"Selemene commands" will return a Luna response (like on the screenshot above). 

All the responses are in lowercase in the dictionary, before comparision the comments are parsed to lowercase as well. Dot or exclamation mark ending the comment is ignored.

*Please note that the bot is not running 24/7, because I run it locally on my computer.*

---
# Changelog:
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
