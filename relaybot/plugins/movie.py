import requests
import json

import plugin


class Movie(plugin.Plugin):
    """Shows movie descriptions from imdb
    """
    def __init__(self, bot):
        super(Movie, self).__init__(bot)
        self.command = "!movie"


    @property
    def description(self):
        return "Shows movie information about a movie from imdb"


    @property
    def long_desc(self):
        return "!movie <title> - show movie information about a movie from imdb"


    @property
    def commands(self):
        return {
            "!movie": "Shows movie information about a movie from imdb"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.movie(' '.join(message.split(' ')[1:])))


    def group_chat_hook(self, groupid, userid, message):
                if message.startswith(self.command):
                    self.bot.user.send_group_msg(groupid, self.movie(' '.join(message.split(' ')[1:])))


    @staticmethod
    def movie(title):
        if len(title) == 0:
            return "Please enter a movie title"

        r = requests.get('http://www.omdbapi.com/?t='+title).text

        parsed = json.loads(r)

        if 'Error' in parsed:
            return parsed['Error'].encode('utf-8')

        seasons = ''
        if 'totalSeasons' in parsed:
            seasons = "Seasons: {}\n".format(parsed['totalSeasons'].encode('utf-8'))

        msg = "Title: {}\nYear: {}\nRuntime: {}\nGenre: {}\nCountry: {}\n{}Plot: {}"\
            .format(parsed['Title'], parsed['Year'], parsed['Runtime'], parsed['Genre'],
                    parsed['Country'], seasons, parsed['Plot']).encode('utf-8')

        return msg

