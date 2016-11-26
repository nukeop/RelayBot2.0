import random
import requests

import plugin

SPOOK_URL = "https://github.com/emacs-mirror/emacs/raw/master/etc/spook.lines"

class Nsa(plugin.Plugin):
    """Shows words from the spook file.
    """
    def __init__(self, bot):
        super(Nsa, self).__init__(bot)
        self.words = self.init_words()
        self.command = "!nsa"


    @property
    def description(self):
        return "Shows words from the emacs spook file."


    @property
    def long_desc(self):
        return ("!nsa will show you one term from the spook file. Adding a"
                " number after the command will show you multiple terms.")


    @property
    def commands(self):
        return {
            "!nsa": "shows one or more terms from the emacs spook file"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.reply(message))


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.reply(message))


    def reply(self, message):
        tokens = message.split()
        if len(tokens)>1:
            try:
                return self.get_words(int(tokens[1]))
            except ValueError:
                return "Invalid argument."
        else:
            return self.get_words()


    def init_words(self):
        words = requests.get(SPOOK_URL).text.encode('utf-8')
        words = words.split('\x00')[1:]

        return words


    def get_words(self, num=1):
        return ' '.join([random.choice(self.words).strip() for _ in
                         range(num)])

