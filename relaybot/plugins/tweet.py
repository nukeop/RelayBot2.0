# -*- coding: utf-8 -*-
import twitter

import plugin
from config import config

TWEET_LIMIT = 140
TWITTER_URL = "https://twitter.com/relay_bot/status/"

class TweetPlugin(plugin.Plugin):
    """Allows authorized users to use Twitter through RelayBot.
    """
    def __init__(self, bot):
        super(TweetPlugin, self).__init__(bot)
        self.command = "!tweet"
        self.twitter = twitter.Twitter(
            auth=twitter.OAuth(
                config["PLUGINS"]["TWITTER_ATOKEN"],
                config["PLUGINS"]["TWITTER_ASECRET"],
                config["PLUGINS"]["TWITTER_CKEY"],
                config["PLUGINS"]["TWITTER_CSECRET"]
            )
        )

    @property
    def description(self):
        return ("Lets users tweet from RelayBot's account.")

    @property
    def long_desc(self):
        return ("Interface to Twitter. The bot's account is at"
                " https://twitter.com/relay_bot . Every tweet will be signed"
                " with the nickname of the user who sent it. ")

    @property
    def commands(self):
        return {
            "!tweet": "tweets whatever you send and signs it with your"
            " nickname"
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.tweet(steamid, message))


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.tweet(userid, message))


    def tweet(self, steamid, message):
        tokens = message.split()
        if len(tokens) > 1:
            tweet = ' '.join(tokens[1:])
            tweet += u'\n―' + self.bot.user.get_name_from_steamid(steamid)

            if len(tweet) <= (TWEET_LIMIT - len(self.bot.user.get_name_from_steamid(steamid)) - 2):
                self.twitter.statuses.update(status=tweet)
                tweetid = self.twitter.statuses.home_timeline(count=1)[0]["id_str"]
                tweeturl = TWITTER_URL + str(tweetid)

                return "Tweet sent.\n\n{}".format(tweeturl)
            else:
                msg = ("Tweet too long, try again. Max length with your"
                       " username: {}. Your tweet is {} characters"
                       " long.".format(
                           TWEET_LIMIT - len(self.bot.user.get_name_from_steamid(steamid)) - 2,
                           len(tweet)
                       )
                )
                return msg
