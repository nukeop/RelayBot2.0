import plugin


class Echo(plugin.Plugin):
    """Lets users join group chats via private chat with the bot.
    """
    def __init__(self, bot):
        super(Echo, self).__init__(bot)
        self.command = "!echo"

        #Dictionary containing users who want to forward messages
        #Keys are user ids, values are group ids
        self.echo_users = {}


    @property
    def description(self):
        return "Lets users join group chats via proxy."


    @property
    def long_desc(self):
        return ("'!echo channels' shows a list of all group chats the bot is"
        " in. '!echo start <group name>' will let you start receiving and"
        " sending messages to/from the group chat, if the bot is in it. '!echo"
        " stop' will stop this. After you start echo, every message from the"
        " group chat will be forwarded to you, and every message you send to"
        " the bot will be forwarded to the group. This enables users using the"
        " mobile app to join group chats.")


    @property
    def commands(self):
        return {
            "!echo": "controls echo functionality. Try '!help Echo' for a more"
            " detailed description."
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.reply(steamid, message))
        elif self.echo_users.get(steamid) is not None:
            self.bot.user.send_group_msg(
                self.echo_users[steamid],
                "{}: {}".format(
                    self.bot.user.get_name_from_steamid(steamid).encode('utf-8'),
                    message.encode('utf-8')
                )
            )


    def group_chat_hook(self, groupid, userid, message):
        for k, v in self.echo_users.iteritems():
            if v == groupid:
                self.bot.user.send_msg(
                    k,
                    "{}: {}".format(
                        self.bot.user.get_name_from_steamid(userid).encode('utf-8'),
                        message.encode('utf-8')
                    )
                )


    def reply(self, steamid, message):
        tokens = message.split()
        if tokens[1] == "channels":
            return '\n'.join(
                "{}. {}".format(i+1, y) for i,y in
                enumerate([self.bot.user.groups.get_name(x) for x in
                           self.bot.user.chats.keys()])
            )
        elif tokens[1] == "start":
            group_names = {self.bot.user.groups.get_name(x).decode('utf-8'): x for x in
                           self.bot.user.chats.keys()}
            group_name = ' '.join(tokens[2:])
            group = group_names.get(group_name)
            if group is None:
                return ("No such group. Try '!echo channels' to see the whole"
                        " list.")
            else:
                self.echo_users[steamid] = group
                return ("Added to channel {}. You will now receive messages from"
                        " this chat.").format(group_name.encode('utf-8'))
        elif tokens[1] == "stop":
            try:
                del self.echo_users[steamid]
            except KeyError:
                return "You are not added to any channel."

            return "Echo stopped. You will no longer receive messages."
