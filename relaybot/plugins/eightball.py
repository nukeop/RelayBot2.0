import random

import plugin

class EightBall(plugin.Plugin):
    """Magic 8ball plugin for private and group chat.
    """
    def __init__(self, bot):
        super(EightBall, self).__init__(bot)

        self.answers = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]

        self.command = "!8ball"

    @property
    def description(self):
        return "Shows a random Magic 8-ball answer to a question."

    @property
    def long_desc(self):
        return ("!8ball or !8ball <question> will show a randomly selected"
        " answer from a classic well-known list.")

    @property
    def commands(self):
        return {
            "!8ball": "shows an answer to a yes/no question"
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, random.choice(self.answers))

    def group_chat_hook(self, groupid, userid, message):
        pass

    def enter_group_chat_hook(self, groupid):
        pass
