import nose
import sys
import unittest

import relaybot.plugins.plugin

from nose.tools import assert_raises

def sanity_test():
    assert True

class Plugin_Tests(unittest.TestCase):

    def setUp(self):
        self.plugin = relaybot.plugins.plugin.Plugin(None)

    def test_description(self):
        with assert_raises(NotImplementedError) as nie:
            desc = self.plugin.description

    def test_long_desc(self):
        with assert_raises(NotImplementedError) as nie:
            desc = self.plugin.long_desc

    def test_init_hook(self):
        assert_raises(NotImplementedError, self.plugin.init_hook)

    def test_private_chat_hook(self):
        assert_raises(NotImplementedError, self.plugin.private_chat_hook, None,
                      None)

    def test_group_chat_hook(self):
        assert_raises(NotImplementedError, self.plugin.group_chat_hook, None,
                      None, None)

    def test_enter_group_chat_hook(self):
        assert_raises(NotImplementedError, self.plugin.enter_group_chat_hook,
                      None) 

