#-*- coding: utf-8 -*-
import nose
import mock
import sys
import unittest

from nose.tools import assert_raises, assert_equal
from steam.enums import EPersonaState

def status(fun):
    def test_new(self, *args, **kwargs):
        print "\nRunning test: {}".format(fun.__name__)
        fun(self, *args, **kwargs)
    return test_new

def sanity_test():
    assert True


class User_Tests(unittest.TestCase):

    def setUp(self):
        bot = mock.Mock()
        client = mock.Mock()
        groups = mock.Mock()

        body = mock.Mock()
        body.persona_name = "RelayBot 2.0 Unit Test"

        first = mock.Mock()
        first.body = body

        def fake_msg(arg):
            return first, 'testval'

        client.wait_event = fake_msg

        import relaybot.user
        self.user = relaybot.user.User(bot, groups, client)

    @status
    def test_change_status(self):
        self.user.change_status(EPersonaState.Online, "test profile name")
        self.user.client.send.assert_called_once()

    @status
    def test_get_name_from_steamid(self):
        def fake_get_user(steamid):
            suser = mock.Mock()
            suser.name = "Test Username"
            return suser
        self.user.client.get_user = fake_get_user

        assert_equal(self.user.get_name_from_steamid(123456789), "Test Username")

    @status
    def test_get_name_from_steamid_failure(self):
        def fake_get_user(steamid):
            suser = mock.Mock()
            suser.name = None
            return suser
        self.user.client.get_user = fake_get_user

        assert_equal(self.user.get_name_from_steamid(123456789), "<unknown>")

    @status
    def test_send_msg(self):
        self.user.send_msg(123456789, "test message")
        self.user.client.send.assert_called_once()

    @status
    def test_auth_code_prompt(self):
        self.user.auth_code_prompt(True, False)
        self.user.client.login.assert_called_once()


class Database_Tests(unittest.TestCase):
    def setUp(self):
        self.sqlite3_mock = mock.MagicMock()

        with mock.patch.dict('sys.modules', {'sqlite3':self.sqlite3_mock}):
            import relaybot.database
            self.db = relaybot.database.Database("test")

    @status
    def test_select(self):
        self.db.select("test", "test1, test2")
        self.db.cursor.execute.assert_called_with("SELECT test1, test2 FROM test")

    @status
    def test_select_condition(self):
        self.db.select("test", "test1, test2", condition="test3")
        self.db.cursor.execute.assert_called_with("SELECT test1, test2 FROM test WHERE test3")

    @status
    def test_create_table(self):
        self.db.create_table("test", "test2")
        self.db.cursor.execute.assert_called_with("CREATE TABLE test(test2)")
        self.db.conn.commit.assert_called_once()

    @status
    def test_insert(self):
        self.db.insert("test1", "test2", "test3", "test4")
        self.db.cursor.execute.assert_called_with("INSERT INTO test1(test2) VALUES (test3)", "test4")
        self.db.conn.commit.assert_called_once()


class Util_Tests(unittest.TestCase):
    @status
    def test_rating_to_stars_full(self):
        import relaybot.util
        assert_equal(relaybot.util.rating_to_stars(5), "★★★★★")

    @status
    def test_rating_to_stars_notfull(self):
        import relaybot.util
        assert_equal(relaybot.util.rating_to_stars(3), "★★★☆☆")

    @status
    def test_rating_to_stars_empty(self):
        import relaybot.util
        assert_equal(relaybot.util.rating_to_stars(0), "☆☆☆☆☆")
