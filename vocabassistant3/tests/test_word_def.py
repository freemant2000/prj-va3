from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.word_def import get_word_defs, get_similar_words, WordDef, get_word_meaning, get_word_meanings

class TestWordDef(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_get_word_def(self):
        wds=get_word_defs(self.s, [1, 2, 4])
        self.assertEquals(len(wds), 3)
        d=wds[0].get_display()
        self.assertTrue("steep" in d)
        self.assertTrue("陡峭" in d)
    def test_display(self):
        wd=WordDef(id=0, word="hand")
        wd.add_meaning("n", "手")
        wd.add_meaning("v", "遞給")
        self.assertEquals(wd.get_display(), "hand\t手(n)、遞給(v)")
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
    def test_get_word_meaning(self):
        wm=get_word_meaning(self.s, 4, 2)
        self.assertEquals(wm.wd.word, "trunk")
        self.assertEquals(wm.meaning, "大木箱")
    def test_get_word_meanings(self):
        wms=get_word_meanings(self.s, [4, 11], [2, 0])
        self.assertEquals(wms[0].wd.word, "trunk")
        self.assertEquals(wms[0].meaning, "大木箱")
        self.assertEquals(wms[1].wd.word, "horn")
        self.assertEquals(wms[1].meaning, "（動物）角")
    def test_add_forms_x2(self):
        wm=get_word_meaning(self.s, 19, 1)
        self.assertEquals(wm.add_forms("fight"), "fight, fought x2")
    def test_add_forms_x3(self):
        wd=WordDef(id=100, word="cut")
        wd.add_meaning("v", "切", ["cut", "cut"])
        self.assertEquals(wd.meanings[0].add_forms("cut"), "cut x3")
    def test_add_forms_normal(self):
        wd=WordDef(id=100, word="lie")
        wd.add_meaning("v", "躺", ["lay", "lain", "lying"])
        self.assertEquals(wd.meanings[0].add_forms("lie"), "lie, lay, lain, lying")
    def test_get_full_word_single_forms(self):
        wd=WordDef(id=100, word="fly")
        wd.add_meaning("v", "飛", ["flew", "flown"])
        wd.add_meaning("n", "蒼蠅")
        self.assertEquals(wd.get_full_word([0]), "fly, flew, flown")
    def test_get_full_word_shared_forms(self):
        wd=WordDef(id=100, word="bear")
        wd.add_meaning("v", "忍受", ["bore", "born"])
        wd.add_meaning("v", "生產", ["bore", "born"])
        wd.add_meaning("n", "熊")
        self.assertEquals(wd.get_full_word([0, 1]), "bear, bore, born")
    def test_get_full_word_diff_forms(self):
        wd=WordDef(id=100, word="hang")
        wd.add_meaning("v", "掛", ["hung", "hung"])
        wd.add_meaning("v", "吊死", ["hanged", "hanged"])
        self.assertEquals(wd.get_full_word([0, 1]), "hang; 0:hung,hung; 1:hanged,hanged")
  
    def test_selected_meanings(self):
        wd=WordDef(id=100, word="cry")
        wd.add_meaning("n", "大叫")
        wd.add_meaning("v", "大叫")
        wd.add_meaning("v", "哭")
        self.assertEquals(wd.get_selected_meanings([0, 2]), "大叫(n)、哭(v)")
    def test_is_usage(self):
        wd=WordDef(id=100, word="cry")
        wd.add_meaning("n", "大叫")
        wd.add_meaning("v", "大叫")
        wd.add_meaning("v", "哭")
        wd2=WordDef(id=100, word="cry")
        wd2.add_meaning("v", "大叫")
        wd2.add_meaning("v", "哭")
        self.assertTrue(wd.is_usage(wd2, "1,2"))
        wd2=WordDef(id=100, word="cry")
        wd2.add_meaning("v", "大叫")
        wd2.add_meaning("v", "哭")
        self.assertFalse(wd.is_usage(wd2, "1,3"))
        wd2=WordDef(id=100, word="abc")
        wd2.add_meaning("v", "大叫")
        wd2.add_meaning("v", "哭")
        self.assertFalse(wd.is_usage(wd2, "1,3"))
        wd2=WordDef(id=100, word="cry")
        wd2.add_meaning("n", "大叫")
        wd2.add_meaning("v", "哭")
        self.assertFalse(wd.is_usage(wd2, "1,2"))

    def test_is_usage_forms(self):
        wd=WordDef(id=100, word="go")
        wd.add_meaning("v", "去", ["went", "gone"])
        wd2=WordDef(id=100, word="go")
        wd2.add_meaning("v", "去")
        self.assertTrue(wd.is_usage(wd2, "0"))
        self.assertTrue(wd.is_usage(wd2, "0F"))

    def test_add_word_def(self):
        self.s.begin()
        wd=WordDef(word="hand")
        wd.add_meaning("n", "手")
        wd.add_meaning("v", "遞給")
        self.s.add(wd)
        self.s.flush()
        wd2=get_word_defs(self.s, [22])
        self.assertEquals(len(wd2), 1)
        d=wd2[0].get_display()
        self.assertTrue("hand" in d)
        self.s.rollback()
        self.reset_word_seq() # seq is done outside transaction
    def reset_word_seq(self):
        set_seq_val(self.s, "word_defs")

