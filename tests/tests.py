import nose
import mock
import sys
import unittest

import relaybot.plugins.plugin
import relaybot.user

from nose.tools import assert_raises, assert_equal
from steam.enums import EPersonaState

def status(fun):
    def test_new(self, *args, **kwargs):
        print "\nRunning test: {}".format(fun.__name__)
        fun(self, *args, **kwargs)
    return test_new

def sanity_test():
    assert True

class Plugin_Tests(unittest.TestCase):

    def setUp(self):
        self.plugin = relaybot.plugins.plugin.Plugin(None)

    @status
    def test_description(self):
        with assert_raises(NotImplementedError) as nie:
            desc = self.plugin.description

    @status
    def test_long_desc(self):
        with assert_raises(NotImplementedError) as nie:
            desc = self.plugin.long_desc

    @status
    def test_init_hook(self):
        assert_raises(NotImplementedError, self.plugin.init_hook)

    @status
    def test_private_chat_hook(self):
        assert_raises(NotImplementedError, self.plugin.private_chat_hook, None,
                      None)

    @status
    def test_group_chat_hook(self):
        assert_raises(NotImplementedError, self.plugin.group_chat_hook, None,
                      None, None)

    @status
    def test_enter_group_chat_hook(self):
        assert_raises(NotImplementedError, self.plugin.enter_group_chat_hook,
                      None)


class User_Tests(unittest.TestCase):

    def setUp(self):
        bot = mock.Mock()
        client = mock.Mock()

        body = mock.Mock()
        body.persona_name = "RelayBot 2.0 Unit Test"

        first = mock.Mock()
        first.body = body

        def fake_msg(arg):
            return first, 'testval'

        client.wait_event = fake_msg

        self.user = relaybot.user.User(bot, client)

    @status
    def test_change_status(self):
        self.user.change_status(EPersonaState.Online, "test profile name")
        self.user.client.send.assert_called_once()

    @status
    def test_get_name_from_steamid(self):
        def fake_get_user(steamid, val):
            suser = mock.Mock()
            suser.name = "Test Username"
            return suser
        self.user.client.get_user = fake_get_user

        assert_equal(self.user.get_name_from_steamid(123456789), "Test Username")

    @status
    def test_send_msg(self):
        self.user.send_msg(123456789, "test message")
        self.user.client.send.assert_called_once()

    @status
    def test_auth_code_prompt(self):
        self.user.auth_code_prompt(True, False)
        self.user.client.login.assert_called_once()
