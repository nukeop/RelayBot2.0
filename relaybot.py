import argparse

import logging
import logging.handlers

VERSION = (2, 0)

logger = logging.getLogger("RelayBot")

import user


class Bot(object):
    """Class initializing and performing high level tasks of the bot. For the
    entire lifetime of the program, there should only exist one instance of
    this. If more than one bot is needed at a time, it should be started from a
    separate copy of the code.
    """
    def __init__(self, logfilename=None):
        logger = self.configure_logging(logfilename)
        self.user = None


    def initialize(self):
        """Performs initialization that needs to happen after the Bot object is
        constructed.
        """
        self.user = user.User()


    def configure_logging(self, logfilename=None):
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
    logger.info("Version: %d.%d", VERSION[0], VERSION[1])

    bot.initialize()

if __name__ == '__main__':
    main()
