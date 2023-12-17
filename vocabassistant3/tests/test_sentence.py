from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.sentence import Sentence, SentenceDraft, add_snt_draft, get_snt, get_snts, get_snts_from_keywords, load_snt_draft, refine_snt_draft
from vocabassistant3.word_def import WordMeaning

class TestWordBank(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_find_snts(self):
        snts=get_snts(self.s, ["squirrel", "river", "trunk"])
        self.assertEquals(len(snts), 4)
        self.assertEquals(snts[0].text, "這條河裡的水在快速地流動。")
    def test_count_matches(self):
        snt=get_snt(self.s, 0)
        self.assertEquals(snt.count_matches(["steep", "egg", "mountain"]), 2)
    def test_find_snts_from_kw(self):
        csnts=get_snts_from_keywords(self.s, ["squirrel", "trunk"])
        self.assertEquals(len(csnts), 3)
        self.assertEquals(csnts[0][0].text, "一隻松鼠爬上了這條樹幹。")
    def test_load_snt_draft(self):
        sd=load_snt_draft("vocabassistant3/tests/test_snt_draft.txt")
        self.assertEquals(sd.text, "這個山谷有巨大的有角的松鼠。")
        self.assertEquals(len(sd.keywords), 3)
        self.assertEquals(len(sd.kw_meanings), 1)
    def test_find_kw_candidates(self):
        sd=load_snt_draft("vocabassistant3/tests/test_snt_draft.txt")
        refine_snt_draft(self.s, sd)
        self.assertEquals(len(sd.kw_meanings), 2)
        self.assertEquals(len(sd.kw_cands), 1)
        self.assertEquals(len(sd.kw_cands["horn"]), 2)        
    def test_find_snt_candidates(self):
        sd=load_snt_draft("vocabassistant3/tests/test_snt_draft2.txt")
        refine_snt_draft(self.s, sd)
        self.assertEquals(len(sd.snt_candidates), 4)
        self.assertEquals(sd.snt_candidates[0].text, "一隻松鼠住在這個山谷裡。")

    def test_add_snt_draft(self):
        self.s.begin()
        sd=SentenceDraft(text="這個山谷有巨大的有角的松鼠。", 
                    keywords=["valley", "squirrel", "horn"],
                    kw_meanings={
                        "valley": WordMeaning(wd_id=5, idx=0, p_of_s="n", meaning="山谷"),
                        "squirrel": WordMeaning(wd_id=4, idx=0, p_of_s="n", meaning="松鼠"),
                        "horn": WordMeaning(wd_id=10, idx=0, p_of_s="n", meaning="（動物）角")})
        add_snt_draft(self.s, sd)
        self.s.flush()
        snt=get_snt(self.s, 11)
        self.assertEquals(snt.text, "這個山谷有巨大的有角的松鼠。")
        self.assertEquals(len(snt.keywords), 3)
        self.s.rollback()
        self.reset_seq()

    def reset_seq(self):
        set_seq_val(self.s, "sentence_seq", 10)
        