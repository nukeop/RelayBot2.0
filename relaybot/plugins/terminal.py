import logging
import shlex
import subprocess

from config import config
import plugin
import relaybot
logger = logging.getLogger(__name__)

class Terminal(plugin.Plugin):
    """Lets authorized users execute arbitrary commands on the same machine
    RelayBot is running.
    """
    def __init__(self, bot):
        super(Terminal, self).__init__(bot)
        self.command = "!terminal"

    @property
    def description(self):
        return "Run commands on the host machine through RelayBot."

    @property
    def long_desc(self):
        return ("!terminal <command> - runs everything after the command"
                "itself as a subprocess.")

    @property
    def commands(self):
        return {
            "!terminal": "runs command on the machine the bot is on"
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):

            if not steamid in config["AUTHORIZED_USERS"]:
                self.bot.user.send_msg(steamid, "Unauthorized user. Access"
                                       " denied.")
                return

            args = message[:-1].split()
            if len(args)>1:
                command = " ".join(args[1:])
                logger.info("Got command: {}".format(command))

                command = shlex.split(command)
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                output = process.communicate()

                if len(output[0]) > 0:
                    self.bot.user.send_msg(steamid, output[0])
                else:
                    self.bot.user.send_msg(steamid, "No output.")
            else:
                self.bot.user.send_msg(steamid, "No arguments.")
