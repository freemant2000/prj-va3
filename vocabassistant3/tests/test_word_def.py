from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.word_def import get_word_defs, get_similar_words, WordDef
from sqlalchemy import text

class TestWordDef(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_get_word_def(self):
        wds=get_word_defs(self.s, [0, 1, 3])
        self.assertEquals(len(wds), 3)
        d=wds[0].get_display()
        self.assertTrue("steep" in d)
        self.assertTrue("陡峭" in d)

    def test_get_similar_words(self):
        wds=get_similar_words(self.s, "f", limit=3)
        self.assertEquals(len(wds), 2)
        self.assertEquals(wds[0].word, "flow")
        self.assertEquals(wds[1].word, "fight")
    
    def test_get_all_m_indice(self):
        wd=WordDef(word="hand")
        wd.add_meaning("n", "手")
        wd.add_meaning("v", "遞給")
        self.assertEquals(wd.get_all_m_indice(), "0,1")

    def test_add_word_def(self):
        self.s.begin()
        wd=WordDef(word="hand")
        wd.add_meaning("n", "手")
        wd.add_meaning("v", "遞給")
        self.s.add(wd)
        wd2=get_word_defs(self.s, [21])
        self.assertEquals(len(wd2), 1)
        d=wd2[0].get_display()
        self.assertTrue("hand" in d)
        self.reset_word_seq() # seq is done outside transaction
        self.s.rollback()

    def reset_word_seq(self):
        set_seq_val(self.s, "word_def_seq", 20)

