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

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.weather(
                ' '.join(message.split(' ')[1:])))

    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.weather(
                ' '.join(message.split(' ')[1:])))

    def weather(self, location):
        if len(location) == 0:
            return "Please enter a location"

        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+location+'&units=metric&APPID='+self.apikey).text
        parsed = json.loads(r)

        weather_conditions = []
        for w in parsed['weather']:
            weather_conditions.append(w['main'])

        msg = "Weather in {}: \nTemperature: {} C\nConditions: {}\nWind speed: {} m/s\nCloudiness: {}%" \
            .format(parsed['name'].encode('utf-8'),parsed['main']['temp'], ', '.join(weather_conditions),
                    parsed['wind']['speed'], parsed['clouds']['all'])
        return msg
