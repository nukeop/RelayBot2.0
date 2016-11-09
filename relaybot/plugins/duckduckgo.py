import json
import requests

import plugin

DDG_API_URL = "https://api.duckduckgo.com/?q={}&format=json"

class DuckDuckGoDefine(plugin.Plugin):
    """Shows definitions of terms retrieved from DuckDuckGo
    """
    def __init__(self, bot):
        super(DuckDuckGoDefine, self).__init__(bot)
        self.command = "!ddg"

    @property
    def description(self):
        return "Shows definitions of terms retrieved from DuckDuckGo."

    @property
    def long_desc(self):
        return ("!ddg <term> - show definition of a term as returned by"
        " DuckDuckGo. If definition cannot be found, instead return related"
        " terms. If there are no related terms, inform about failure.")

    @property
    def commands(self):
        return {
            "!ddg": "shows definitions from DuckDuckGo"
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.ddg_def(
                ' '.join(message.split(' ')[1:])))

    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.ddg_def(
                ' '.join(message.split(' ')[1:])))

    @staticmethod
    def ddg_def(term):
        url = DDG_API_URL.format(term)
        text = requests.get(url).text
        parsed = json.loads(text)

        abstract = parsed['AbstractText']
        abstracturl = parsed['AbstractURL']

        if abstract == "":
            related = parsed['RelatedTopics']
            relatedstr = ""

            if len(related) < 1:
                return "No information about term {}.".format(term)

            for i, entry in enumerate(related):
                try:
                    relatedstr += "({}) {}\n".format(i+1, entry['Text'])
                except KeyError:
                    pass

            return relatedstr

        return (abstract + '\n' + abstracturl).encode('utf-8')
