# -*- coding: utf-8 -*-
import twitter

import plugin
from config import config

TWEET_LIMIT = 140

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
            tokens = message.strip().strip('\x00').split()
            if len(tokens) > 1:
                tweet = ' '.join(tokens[1:]).decode('utf-8')
                tweet += '\n' + u'―' + self.bot.user.get_name_from_steamid(steamid)

                if len(tweet) <= (TWEET_LIMIT - len(self.bot.user.get_name_from_steamid(steamid)) - 2):
                    self.twitter.statuses.update(status=tweet)
                    self.bot.user.send_msg(steamid, "Tweet sent.")
                else:
                    msg = ("Tweet too long, try again. Max length with your"
                           " username: {}. Your tweet is {} characters"
                           " long.".format(
                               TWEET_LIMIT - len(self.bot.user.get_name_from_steamid(steamid)) - 2,
                               len(tweet)
                           )
                    )
                    self.bot.user.send_msg(steamid, msg)
