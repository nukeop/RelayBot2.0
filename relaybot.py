import argparse
import steam.client

import logging

VERSION = (2, 0)

logger = logging.getLogger("RelayBot")

import config
import user


class Bot(object):
    def __init__(self):
        logger = self.configure_logging()

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
    bot = Bot()

    logger.info("Starting Relay Bot 2.0")
    logger.info("Version: {}.{}".format(VERSION[0], VERSION[1]))

    u = user.User()


if __name__ == '__main__':
    main()
