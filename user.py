import steam.client
from steam.enums import EResult
from steam.enums.emsg import EMsg

import logging
import os
import time

import config
import relaybot

logger = logging.getLogger("{}.{}".format(relaybot.logger.name,  __name__))

class User(object):

    client = steam.client.SteamClient()

    def __init__(self):
        logger.info("Creating a User instance")
        User.client.set_credential_location(os.getcwd())
        if User.client.relogin_available:
            User.client.relogin()
        else:
            User.client.login(config.user, config.pwd)

        msg, = User.client.wait_event(EMsg.ClientAccountInfo)
        logger.info("Logged in as {}".format(msg.body.persona_name.encode('utf-8')))
        logger.info("SteamID: {}".format(repr(User.client.steam_id)))

        time.sleep(5)

    @client.on('error')
    def handle_errors(result):
        print "Error: ", EResult(result)

    @client.on('auth_code_required')
    def auth_code_prompt(is_2fa, code_mismatch):
        if is_2fa:
            code = raw_input("Enter Steam Mobile Authenticator code: ")
            User.client.login(config.user, config.pwd, two_factor_code=code)
        else:
            code = raw_input("Enter Steam Guard code: ")
            User.client.login(config.user, config.pwd, auth_code=code)

