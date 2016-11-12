import logging
import sys

from traceback import format_exception

logger = logging.getLogger(__name__)


def exc_handler(type, value, traceback):
    logger.error(''.join(format_exception(type, value, traceback)))


def set_exception_handler():
    sys.excepthook = exc_handler
