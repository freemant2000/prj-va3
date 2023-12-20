from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.word_bank import WordBankDraft, find_word_banks, load_wb_input, get_word_bank, add_wb_draft
from vocabassistant3.word_def import WordDef, WordMeaning, WordUsage

class TestWordBank(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_load_draft(self):
        wbd=load_wb_input("vocabassistant3/tests/test_wb_draft.txt")
        self.assertEquals(wbd.name, "fisherman-and-wife-1")
        self.assertEquals(len(wbd.wds), 11)
        self.assertEquals(wbd.wds[0].word, "humble")
        self.assertEquals(len(wbd.word_usages), 1)
    def test_get_word_bank(self):
        wb=get_word_bank(self.s, 1)
        self.assertEquals(len(wb.bws), 13)
    def test_find_word_banks_name(self):
        wbs=find_word_banks(self.s, "jackal")
        self.assertEquals(len(wbs), 1)
        self.assertEquals(wbs[0].name, "fighting-goats-and-jackal-level-2")
    def test_find_word_banks_word(self):
        wbs=find_word_banks(self.s, "river")
        self.assertEquals(len(wbs), 1)
        self.assertEquals(wbs[0].name, "two-goats-level-2")
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
        wbd.word_usages[wd]=WordUsage(
            WordDef(id=1, word="mountain", meanings=[WordMeaning(wd_id=1, p_of_s="n", meaning="山")]),
            m_indice="0")
        add_wb_draft(self.s, wbd)
        self.s.flush()
        wb=get_word_bank(self.s, 3)
        self.assertEquals(wb.name, "my wb1")
        self.assertEquals(len(wb.bws), 2)
        self.s.rollback()
        self.reset_word_seq() # seq is done outside transaction

    def reset_word_seq(self):
        set_seq_val(self.s, "word_defs")
        set_seq_val(self.s, "word_banks")
