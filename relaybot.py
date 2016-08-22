import argparse

import logging

VERSION = (2, 0)

logger = logging.getLogger("RelayBot")

import user


class Bot(object):
    """Class initializing and performing high level tasks of the bot. For the
    entire lifetime of the program, there should only exist one instance of
    this. If more than one bot is needed at a time, it should be started from a
    separate copy of the code.
    """
    def __init__(self):
        logger = self.configure_logging()
        self.user = None


    def initialize(self):
        """Performs initialization that needs to happen after the Bot object is
        constructed.
        """
        self.user = user.User()


    def configure_logging(self):
        """Creates a root logger, configures it, and returns it.
        """
        root = logging.getLogger("RelayBot")
        root.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(levelname)s] - %(asctime)s - %(name)s -"
        " %(message)s")

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)

        root.addHandler(console)

        return root


def main():
    """RelayBot 2.0 main entry point.
    Creates a new instance of the bot and runs it.
    """
    parser = argparse.ArgumentParser()
    args = parser.parse_args()


    bot = Bot()

    logger.info("Starting Relay Bot 2.0")
    logger.info("Version: {}.{}".format(VERSION[0], VERSION[1]))

    bot.initialize()

if __name__ == '__main__':
    main()
