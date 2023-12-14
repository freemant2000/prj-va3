from unittest import TestCase
from vocabassistant3.db_base import open_session
from vocabassistant3.word_bank import load_wb_input, get_word_bank

class TestWordBank(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_load_draft(self):
        wbd=load_wb_input("vocabassistant3/tests/test_wb_input.txt")
        self.assertEquals(wbd.name, "fisherman-and-wife-1")
        self.assertEquals(len(wbd.wds), 11)
        self.assertEquals(wbd.wds[0].word, "humble")
        self.assertEquals(len(wbd.use_old_wds), 1)
    def test_get_word_bank(self):
        wb=get_word_bank(self.s, 0)
        self.assertEquals(len(wb.bws), 13)
