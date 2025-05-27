from unittest import TestCase
from test_db_connector import open_session
from vocabassistant3.practice import get_all_bws

class TestStud(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()

    def test_get_all_bws(self):
        bws=get_all_bws(self.s, 1)
        self.assertEquals(len(bws), 20)
        self.assertEquals(bws[0].get_meanings(), "陡峭（斜）的(adj)")
        