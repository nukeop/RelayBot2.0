import json
import requests

import plugin
from config import config

PLAYER_API_URL = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?"

class Games(plugin.Plugin):
    """Shows info about user's recently played games using Steam API.
    """
    def __init__(self, bot):
        super(Games, self).__init__(bot)
        self.command = "!games"

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
        games = ["{}'s stats:".format(username)]
        for game in reply['response']['games']:
            games.append("{}, last 2 weeks: {}, total: {}".format(
                game['name'],
                game['playtime_2weeks'],
                game['playtime_forever']
            ))

        return '\n'.join(games)


