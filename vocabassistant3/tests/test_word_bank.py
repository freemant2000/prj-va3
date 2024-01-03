from unittest import TestCase
from vocabassistant3.tests.test_db_connector import open_session
from vocabassistant3.db_base import set_seq_val
from vocabassistant3.word_bank import BankWord, WordBankDraft, find_word_banks, load_wb_draft, get_word_bank, add_wb_draft, parse_full_word, refine_wb_draft
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
    def test_get_full_word_single_forms(self):
        wd=WordDef(id=100, word="fly")
        wd.add_meaning("v", "飛", ["flew", "flown"])
        wd.add_meaning("n", "蒼蠅")
        bw=BankWord(wd=wd, m_indice="0F,1")
        self.assertEquals(bw.get_full_word(), "fly, flew, flown")
    def test_get_full_word_shared_forms(self):
        wd=WordDef(id=100, word="bear")
        wd.add_meaning("v", "忍受", ["bore", "born"])
        wd.add_meaning("v", "生產", ["bore", "born"])
        wd.add_meaning("n", "熊")
        bw=BankWord(wd=wd, m_indice="0F,1F,2")
        self.assertEquals(bw.get_full_word(), "bear, bore, born")
    def test_get_full_word_diff_forms(self):
        wd=WordDef(id=100, word="hang")
        wd.add_meaning("v", "掛", ["hung", "hung"])
        wd.add_meaning("v", "吊死", ["hanged", "hanged"])
        bw=BankWord(wd=wd, m_indice="0F,1F")
        self.assertEquals(bw.get_full_word(), "hang; 0:hung,hung; 1:hanged,hanged")
    def test_get_meanings(self):
        wd=WordDef(id=100, word="fly")
        wd.add_meaning("v", "飛", ["flew", "flown"])
        wd.add_meaning("n", "蒼蠅")
        bw=BankWord(wd=wd, m_indice="0F")
        self.assertEquals(bw.get_meanings(), "飛(v)")
        bw=BankWord(wd=wd, m_indice="0F,1")
        self.assertEquals(bw.get_meanings(), "飛(v)、蒼蠅(n)")
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
    def test_strict_cands(self):
        wbd=WordBankDraft()
        wd1=WordDef(word="us")
        wd2=WordDef(word="US")
        wd3=WordDef(word="us")
        wbd.cands[wd1]=[wd2, wd3]
        self.assertEquals(len(wbd.get_strict_cands()[wd1]), 1)
        wbd=WordBankDraft()
        wd1=WordDef(word="us")
        wd2=WordDef(word="US")
        wbd.cands[wd1]=[wd2]
        self.assertEquals(len(wbd.get_strict_cands()), 0)
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
    def test_parse_updates(self):
        try:
            load_wb_draft("vocabassistant3/tests/test_wb_draft6.txt")
            self.fail()
        except ValueError:
            pass
    def test_refine_question_mark(self):
        wbd=load_wb_draft("vocabassistant3/tests/test_wb_draft7.txt")
        refine_wb_draft(self.s, wbd)
        self.assertEquals(len(wbd.word_usages), 3)
        self.assertEquals(wbd.word_usages[wbd.wds[0]].wd.id, 4)
        self.assertEquals(wbd.word_usages[wbd.wds[1]].wd.id, 3)
        self.assertEquals(wbd.word_usages[wbd.wds[2]].wd.id, 6)
        self.assertEquals(len(wbd.mismatches), 1)
        wms=wbd.wds[0].meanings
        self.assertEquals(len(wms), 1)
        self.assertEquals(wms[0].meaning, "象鼻")
    def test_refine_wb_draft_infer(self):
        wbd=WordBankDraft(name="my wb1")
        wd=WordDef(word="trunk")
        wd.add_meaning("n", "象鼻")
        wbd.wds.append(wd)
        refine_wb_draft(self.s, wbd)
        self.assertEquals(len(wbd.word_usages), 1)
        wu=wbd.word_usages[wd]
        self.assertEquals(wu.wd.id, 4)
        self.assertEquals(wu.m_indice, "1")
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
            WordDef(id=2, word="mountain", meanings=[WordMeaning(wd_id=2, p_of_s="n", meaning="山")]),
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
