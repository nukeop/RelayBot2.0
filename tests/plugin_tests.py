import json
import nose
import mock
import unittest

from nose.tools import assert_equal, assert_in
from tests import status


class Eightball_Tests(unittest.TestCase):
    def setUp(self):
        bot = mock.Mock()
        from relaybot.plugins import eightball
        self.eightball = eightball.EightBall(bot)

    @status
    def test_answer(self):
        ans = self.eightball.get_answer()
        assert_in(ans, self.eightball.answers)

class DuckDuckGo_Tests(unittest.TestCase):
    def setUp(self):
        bot = mock.Mock()
        self.requests_mock = mock.MagicMock()

        with mock.patch.dict('sys.modules', {'requests': self.requests_mock}):
            import relaybot.plugins.duckduckgo
            self.ddg = relaybot.plugins.duckduckgo.DuckDuckGoDefine(bot)

    @status
    def test_ddg_def(self):
        import json

        fake_value = json.dumps({'AbstractText':"test1", 'AbstractURL':"test2"})
        fake_response = mock.MagicMock()
        fake_response.text = fake_value

        self.requests_mock.get = mock.MagicMock(return_value=fake_response)

        import relaybot.plugins.duckduckgo
        with mock.patch.dict(self.ddg.ddg_def.func_globals,
                             {
                                 'requests': self.requests_mock,
                                 'json':json,
                                 'DDG_API_URL':relaybot.plugins.duckduckgo.DDG_API_URL
                             }):
            ans = self.ddg.ddg_def("test")
            assert_equal(ans, "test1\ntest2")


    @status
    def test_ddg_def_related(self):

        fake_value = json.dumps({'AbstractText':"",
                                 'AbstractURL':"",
                                 'RelatedTopics':[{'Text':"test1"}, {'Text':"test2"}, {'Text':"test3"}]})
        fake_response = mock.MagicMock()
        fake_response.text = fake_value

        self.requests_mock.get = mock.MagicMock(return_value=fake_response)

        with mock.patch.dict(self.ddg.ddg_def.func_globals,
                             {'requests': self.requests_mock, 'json':json}):
            ans = self.ddg.ddg_def("test")
            assert_equal(ans, ''.join(['({}) test{}\n'.format(x, x) for x in range(1, 4)]))


    @status
    def test_ddg_def_notfound(self):
        fake_value = json.dumps({'AbstractText':"",
                                 'AbstractURL':"",
                                 'RelatedTopics':[]})

        fake_response = mock.MagicMock()
        fake_response.text = fake_value

        self.requests_mock.get = mock.MagicMock(return_value=fake_response)

        with mock.patch.dict(self.ddg.ddg_def.func_globals,
                             {'requests': self.requests_mock, 'json':json}):
            ans = self.ddg.ddg_def("test")
            assert_equal(ans, "No information about term test.")
