import logging

import plugin
import config

logger = logging.getLogger(__name__)

class SilencePlugin(plugin.Plugin):
    """Enables admin users and group authorities to silence the bot or permit
    it to speak again.
    """
    def __init__(self, bot):
        super(SilencePlugin, self).__init__(bot)
        self.command = "!silence"


    @property
    def description(self):
        return ("Makes me stop talking in the group chat, or lets me start"
                " talking again.")


    @property
    def long_desc(self):
        return ("!silence can be used to toggle the bot between muted and"
                "normal states. This can only be toggled by admins and users"
                " who have some authority in the group (admins, owners,"
                " moderators, etc.). If the bot is muted it will be prevented"
                "from sending any messages to the chat.")


    @property
    def commands(self):
        return {
            "!silence": "mutes the bot in the group chat or lets it speak"
            "again"
        }


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            #ignore command if issued by a non-admin or regular member
            if not (userid in config.config["AUTHORIZED_USERS"] or
                    util.has_authority(self.bot, userid, groupid)):
                return

            self.bot.user.send_group_msg(groupid, self.toggle_silenced(groupid))


    def toggle_silenced(self, groupid):
        """Checks if the bot is silenced in a group and toggles the status.
        """
        if not groupid in config.config["SILENCED"]:
            self.silence(groupid)
            return "I will not talk anymore here."
        else:
            self.unsilence(groupid)
            return "I will start talking here."


    def silence(self, groupid):
        """Adds a group to silenced groups in the config and saves it.
        """
        if not groupid in config.config["SILENCED"]:
            try:
                config.add_to(groupid, "SILENCED")
            except ValueError:
                logger.error("Invalid group id, could not add to silenced.")


    def unsilence(self, groupid):
        """Removes a group from the silenced list in the config and saves it.
        """
        if not groupid in config.config["SILENCED"]:
            logger.error("Not silenced in this group.")
            return

        try:
            config.remove_from(groupid, "SILENCED")
        except ValueError:
            logger.error("Invalid group id, could not remove from silenced.")

