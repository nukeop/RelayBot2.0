import argparse
import logging
import logging.handlers
import os

import steam.client

VERSION = (2, 0.2)

logger = logging.getLogger()

import database
import plugins
import user

class Bot(object):
    """Class initializing and performing high level tasks of the bot. For the
    entire lifetime of the program, there should only exist one instance of
    this. If more than one bot is needed at a time, it should be started from a
    separate copy of the code.
    """
    def __init__(self, logfilename=None):
        self.configure_logging(logfilename)
        self.user = None

        self.database = database.Database('relaybot.db')

        self.import_plugins()
        self.plugins = []

        for plugin in plugins.plugin.Plugin.__subclasses__():
            plugininst = plugin(self)
            self.plugins.append(plugininst)

    def import_plugins(self):
        logger.info("Scanning plugins...")
        files = os.listdir(os.path.join(os.path.dirname(__file__),
                                        plugins.__name__))
        files = [os.path.splitext(x)[0] for x in files if
                 os.path.splitext(x)[1] == ".py"
                 and "__init__" not in x]

        for module in files:
            logger.info("Detected plugin: %s", module)
            try:
                __import__("plugins.{}".format(module))
            except Exception as e:
                logger.error("Invalid plugin: %s", module)
                logger.error(str(e))

    def initialize(self):
        """Performs initialization that needs to happen after the Bot object is
        constructed.
        """
        self.user = user.User(self, steam.client.SteamClient())

    def run(self):
        """Starts the main loop, handles logout on interrupt.
        """
        try:
            self.user.client.run_forever()
        except KeyboardInterrupt:
            self.user.client.logout()

    def configure_logging(self, logfilename=None):
        """Creates a root logger, configures it, and returns it.
        """
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        logging.getLogger('SteamClient').setLevel(logging.WARNING)

        formatter = logging.Formatter("[%(levelname)s] - %(asctime)s - %(name)s -"
        " %(message)s")

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        root.addHandler(console)

        if logfilename is not None:
            rfhandler = logging.handlers.RotatingFileHandler(logfilename,
                        maxBytes=2*1024*1024,
                        backupCount=8)
            rfhandler.setLevel(logging.DEBUG)
            rfhandler.setFormatter(formatter)
            root.addHandler(rfhandler)

        return root

def main():
    """RelayBot 2.0 main entry point.
    Creates a new instance of the bot and runs it.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--logfile", help="rotating log filename")
    args = parser.parse_args()

    bot = Bot(args.logfile)

    logger.info("Starting Relay Bot 2.0")
    logger.info("Version: {}.{}".format(VERSION[0], VERSION[1]))

    bot.initialize()

    bot.run()


if __name__ == '__main__':
    main()
