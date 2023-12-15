from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.word_bank import WordBankDraft, WordBankItemOld, load_wb_input, get_word_bank, add_wb_draft
from vocabassistant3.word_def import WordDef
from sqlalchemy import text

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
    def test_add_draft(self):
        self.s.begin()
        wbd=WordBankDraft(name="my wb1")
        wd=WordDef(word="sick")
        wd.add_meaning("adj", "病的")
        wd.add_meaning("adj", "想嘔的")
        wd.add_meaning("adj", "厭倦的")
        wbd.wds.append(wd)
        wd=WordDef(word="mountain")
        wd.add_meaning("n", "山")
        wbd.wds.append(wd)
        wbd.use_old_wds[wd]=WordBankItemOld(1, "0")
        add_wb_draft(self.s, wbd)
        wb=get_word_bank(self.s, 11)
        self.assertEquals(wb.name, "my wb1")
        self.assertEquals(len(wb.bws), 2)
        self.reset_word_seq() # seq is done outside transaction
        self.s.rollback()

    def reset_word_seq(self):
        set_seq_val(self.s, "word_def_seq", 20)
        set_seq_val(self.s, "word_bank_seq", 10)
