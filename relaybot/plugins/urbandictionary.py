import json
import requests

import plugin

UD_API_URL = "http://api.urbandictionary.com/v0/define?term={}"

RESULT_NO_RESULTS = "no_results"
RESULT_EXACT = "exact"


class UrbanDictionary(plugin.Plugin):
    """Shows definitions of terms retrieved from Urban Dictionary
    """
    def __init__(self, bot):
        super(UrbanDictionary, self).__init__(bot)
        self.command = "!urban"

    @property
    def description(self):
        return "Shows definitions of terms retrieved from DuckDuckGo."

    @property
    def long_desc(self):
        return ("!urban <term> - show definition of a term as returned by"
                " Urban Dictionary. If it doesn't exist, inform the user. "
                "If there are more definitons, inform the user too."
                "\n!urban <number> <term> - show <number> definitions for"
                " a term, or all of them if there are less than <number>.")

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):

            args = message[:-1].split(' ')
            if len(args) < 2:
                return "Try !urban <term>."
            num = 1
            num_in_args = False
            try:
                num = int(args[1])
                num_in_args = True
            except ValueError:
                pass

            msg = None
            if num_in_args:
                msg = self.ud_def(' '.join(args[2:]), num)
            else:
                msg = self.ud_def(' '.join(args[1:]), num)

            self.bot.user.send_msg(steamid, msg)

    def group_chat_hook(self, groupid, userid, message):
        pass

    def enter_group_chat_hook(self, groupid):
        pass

    @staticmethod
    def ud_def(term, num):
        print term
        url = UD_API_URL.format(term)
        text = requests.get(url).text
        parsed = json.loads(text)

        if parsed["result_type"] == RESULT_NO_RESULTS:
            return "No results for {}.".format(term)

        if parsed["result_type"] == RESULT_EXACT:
            msg = ""
            for i, entry in enumerate(parsed['list']):
                if i < num:
                    print entry['definition']
                    msg += "({}) {}\n".format(i+1,
                                        entry['definition'].encode('utf-8'))
                else:
                    break

            return msg
