import datetime
import json
import time

import requests
from eventregistry import *

import plugin

class SpillTheBeans(plugin.Plugin):
    """Shows news on any topic.
    """
    def __init__(self, bot):
        super(SpillTheBeans, self).__init__(bot)
        self.command = "!spillthebeans"
        self.er = EventRegistry()
        self.query = QueryArticles()


    @property
    def description(self):
        return "Shows recent news about any topic."


    @property
    def long_desc(self):
        return ("!spillthebeans <topic> uses EventRegistry to fetch articles"
                "about any keywords. It will only look for articles in"
                " English and ones that were posted in the last month. The"
                " most recent article is returned and shown to the user.")


    @property
    def commands(self):
        return {
            "!spillthebeans": "shows recent news about any topic"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.get_news(message))


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.get_news(message))


    def get_news(self, message):
        term = ' '.join(message.split()[1:])
        if len(term) == 0:
            return "No search terms provided."

        #Month ago
        date = datetime.datetime.fromtimestamp(time.time() - 60 * 60 * 30)
        date = "{}-{}-{}".format(date.year, date.month, date.day)

        self.query = QueryArticles(lang='eng',
                                   dateStart=date,
                                   conceptUri=self.er.getConceptUri(term)
        )
        self.query.addRequestedResult(RequestArticlesInfo(sortBy = "date",
                                                          count=1))

        results = self.er.execQuery(self.query)
        try:
            article = results['articles']['results'][0]

            return "{}\n{} {}\n\n{}\n{}".format(article['title'],
                                                article['date'],
                                                article['time'],
                                                article['body'],
                                                article['url']
            )
        except KeyError:
            return "No news about {}.".format(term)
