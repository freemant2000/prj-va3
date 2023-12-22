from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.word_bank import WordBankDraft, find_word_banks, load_wb_draft, get_word_bank, add_wb_draft, parse_full_word
from vocabassistant3.word_def import WordDef, WordMeaning, WordUsage, get_word_def_by_id

class TestWordBank(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_load_draft(self):
        wbd=load_wb_draft("vocabassistant3/tests/test_wb_draft.txt")
        self.assertEquals(wbd.name, "fisherman-and-wife-1")
        self.assertEquals(len(wbd.wds), 11)
        self.assertEquals(wbd.wds[0].word, "humble")
        self.assertEquals(len(wbd.word_usages), 1)
    def test_get_word_bank(self):
        wb=get_word_bank(self.s, 1)
        self.assertEquals(len(wb.bws), 13)
    def test_get_full_word(self):
        wb=get_word_bank(self.s, 3)
        self.assertEquals(wb.bws[0].get_full_word(), "fight, fought x2")
        self.assertEquals(wb.bws[1].get_full_word(), "person, people")
    def test_find_word_banks_name(self):
        wbs=find_word_banks(self.s, "jackal")
        self.assertEquals(len(wbs), 1)
        self.assertEquals(wbs[0].name, "fighting-goats-and-jackal-level-2")
    def test_find_word_banks_word(self):
        wbs=find_word_banks(self.s, "river")
        self.assertEquals(len(wbs), 1)
        self.assertEquals(wbs[0].name, "two-goats-level-2")
    def test_parse_full_word(self):
        word, forms=parse_full_word("go, went, gone")
        self.assertEquals(word, "go")
        self.assertEquals(forms, ["went", "gone"])        
    def test_parse_forms(self):
        wbd=load_wb_draft("vocabassistant3/tests/test_wb_draft3.txt")
        self.assertEquals(wbd.wds[0].meanings[0].get_forms(), ["went", "gone"])
        self.assertEquals(wbd.wds[1].meanings[0].get_forms(), ["teeth"])
        self.assertEquals(wbd.wds[2].meanings[0].get_forms(), ["hung", "hung"])
        self.assertEquals(wbd.wds[2].meanings[1].get_forms(), ["hanged", "hanged"])
    def test_parse_updates(self):
        wbd=load_wb_draft("vocabassistant3/tests/test_wb_draft5.txt")
        self.assertEquals(len(wbd.word_updates), 2)
        self.assertEquals(wbd.word_updates[wbd.wds[0]], 7)
        self.assertEquals(wbd.word_updates[wbd.wds[1]], 19)
        self.assertEquals(wbd.wds[0].word, "rock")
        self.assertEquals(wbd.wds[1].word, "fight")
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
        wb=get_word_bank(self.s, 4)
        self.assertEquals(wb.name, "my wb1")
        self.assertEquals(len(wb.bws), 2)
        self.s.rollback()
        self.reset_word_seq() # seq is done outside transaction

    def test_add_draft_upd(self):
        self.s.begin()
        wbd=WordBankDraft(name="my wb1")
        wd=WordDef(id=7, word="rock")
        wd.add_meaning("n", "岩石")
        wd.add_meaning("v", "遙動")
        wbd.wds.append(wd)
        wbd.word_updates[wd]=7
        wbd.upd_targets[wd]=get_word_def_by_id(self.s, 7)
        add_wb_draft(self.s, wbd)
        self.s.flush()
        wb=get_word_bank(self.s, 4)
        self.assertEquals(wb.name, "my wb1")
        self.assertEquals(len(wb.bws), 1)
        self.assertEquals(len(wb.bws[0].wd.meanings) ,2)
        self.s.rollback()
        self.reset_word_seq() # seq is done outside transaction

    def reset_word_seq(self):
        set_seq_val(self.s, "word_defs")
        set_seq_val(self.s, "word_banks")
