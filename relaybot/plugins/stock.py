import requests

import plugin

YAHOO_API_URL = "http://finance.yahoo.com/d/quotes.csv?s={}&f=snl1"

class Stock(plugin.Plugin):
    """Shows current value of a company's stock
    """
    def __init__(self, bot):
        super(Stock, self).__init__(bot)
        self.command = "!stock"

    @property
    def description(self):
        return "Shows current value of a company's stock."

    @property
    def long_desc(self):
        return ("!stock <symbol> - return current stock value.")

    @property
    def commands(self):
        return {
            "!stock": "shows current stock value"
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.get_stock(
                ' '.join(message.split(' ')[1:])))

    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.get_stock(
                ' '.join(message.split(' ')[1:])))


    @staticmethod
    def get_stock(symbol):
        url = YAHOO_API_URL.format(symbol)
        text = requests.get(url).text.replace('"', '')
        tokens = text.split(',')
        symbol = tokens[0]
        name = ' '.join(tokens[1:-1])
        value = tokens[len(tokens)-1]

        if name == 'N/A' or value == 'N/A':
            return ("Could not retrieve stock value for symbol"
            " {}.").format(symbol.upper())

        return "Stock value for symbol {} ({}): {}".format(symbol.upper(),
                                                           name,
                                                           value)
