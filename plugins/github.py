import github3

import plugin

RELAYBOT_REPO = "Relaybot2.0"
GITHUB_USER = ""
GITHUB_PASSW = ""

class Github(plugin.Plugin):
    """Interface between Steam chat and Github repo.
    Lets users check the latest commits in the RelayBot2.0 repository, and
    allows authorized users to upload new plugins using steam chat. The bot
    will create a new branch, upload the code as a new plugin file, and create
    a pull request.
    """
    def __init__(self, bot):
        super(Github, self).__init__(bot)
        self.command = "!github"
        self.gh = github3.login(GITHUB_USER, password=GITHUB_PASSW)

    @property
    def description(self):
        return ("An interface between Github and Steam. Lets you check out"
                "latest changes.")

    @property
    def long_desc(self):
        return ("!github commits - see the last five commits to the main"
                "branch")

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            if 'commits' in message:
                self.bot.user.send_msg(steamid, self.build_commit_string())

    def build_commit_string(self):
        repo = self.gh.repository(self.gh.user(), RELAYBOT_REPO)
        result = ""

        for i, c in enumerate(repo.iter_commits()):
            result += "Link: {}\n".format(c.html_url)
            result += "Author: {}\n".format(c.author)
            result += "Comment: {}\n".format(c.commit.message)
            result += "\n"
            if i>3:
                break

        return result

    def group_chat_hook(self, groupid, userid, message):
        pass

    def enter_group_chat_hook(self, groupid):
        pass
