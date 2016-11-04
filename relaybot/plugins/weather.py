import requests
import json

import plugin
from config import config

class Weather(plugin.Plugin):
    """Shows weather conditions retrieved from OpenWeatherMap
    """
    def __init__(self, bot):
        super(Weather, self).__init__(bot)
        self.command = "!weather"
        self.bot = bot
        self.apikey = config['PLUGINS']['OPENWEATHERMMAP_APIKEY']

    @property
    def description(self):
        return "Shows weather conditions from OpenWeatherMap."


    @property
    def long_desc(self):
        return ("!weather <location> - show temperature in location")

    @property
    def commands(self):
        return {
            "!weather": "Shows basic weather conditions from OpenWeatherMap"
        }

    def init_hook(self):
        """This will be registered and called exactly once when the bot
        initializes itself.
        """
        pass

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.weather(
                ' '.join(message[:-1].split(' ')[1:])))
        pass

    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(groupid, self.weather(
                ' '.join(message[:-1].split(' ')[1:])))
        pass
        pass

    def enter_group_chat_hook(self, groupid):
        pass

    def user_entered_hook(self, groupid, userid):
        """Called whenever a user enters a group chat the bot is in.
        """
        pass

    def user_left_hook(self, groupid, userid):
        """Called whenever a user leaves a group chat the bot is in.
        """
        pass

    def weather(self, location):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+location+'&units=metric&APPID='+self.apikey).text
        parsed = json.loads(r)

        weather_conditions = []
        for w in parsed['weather']:
            weather_conditions.append(w['main'])

        msg = "Weather in " + parsed['name'] + ":\nTemperature: " + str(parsed['main']['temp']) + ' C\nConditions: ' + \
              ', '.join(weather_conditions) + "\nWind speed: " + str(parsed['wind']['speed']) + ' m/s\nCloudiness: ' + str(parsed['clouds']['all']) \
              + '%'

        return msg

