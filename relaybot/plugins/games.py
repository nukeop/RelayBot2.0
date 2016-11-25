import json
import requests

import plugin
import util
from config import config

PLAYER_API_URL = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?"

class Games(plugin.Plugin):
    """Shows info about user's recently played games using Steam API.
    """
    def __init__(self, bot):
        super(Games, self).__init__(bot)
        self.command = "!games"


    @property
    def description(self):
        return "Shows information about users' recently played games."


    @property
    def long_desc(self):
        return ("!games <username> will display stats about games that user"
        " played in the last two weeks. The user must be currently in the same"
        " group as the bot. That user's profile must be public, or if it's"
        " friends only, the bot must be the user's friend.")


    @property
    def commands(self):
        return {
            "!games": "shows info about a user's most recently played games"
        }


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.get_games(groupid,
                                                                 message))


    def get_games(self, groupid, message):
        username = ' '.join(message.split()[1:])
        steamid = self.bot.user.username_to_steamid(groupid, username)

        if not steamid:
            return "Unknown user {}.".format(username)

        params = {
            'key': config['STEAM_API_KEY'],
            'steamid': steamid,
            'format': 'json'
        }

        reply = json.loads(requests.get(PLAYER_API_URL, params=params).text)

        if len(reply['response']) == 0:
            return "{}'s profile is private.".format(username)

        if reply['response']['total_count'] == 0:
            return "{} hasn't played any games recently.".format(username)

        games = ["{}'s stats:".format(username)]
        for game in reply['response']['games']:
            games.append("{}, last 2 weeks: {}, total: {}".format(
                game['name'],
                "{} hrs {} min".format(
                    *util.minutes_to_hours(game['playtime_2weeks'])
                ),
                "{} hrs {} min".format(
                    *util.minutes_to_hours(game['playtime_forever'])
                )
            ))

        return '\n'.join(games)


