from unittest import TestCase
from vocabassistant3.va3 import *

class TestVA3(TestCase):
    def test_find(self):
        snts=find_sentences(["squirrel", "river", "trunk"])
        self.assertEquals(len(snts), 4)
        self.assertEquals(snts[0], u"一隻松鼠爬上了這條樹幹。")

    def test_get_wd_in_sprint(self):
        snts=get_wd_in_sprint(0)
        self.assertEquals(len(snts), 13)

    def test_get_wd_in_exercise(self):
        snts=get_wd_in_exercise(0)
        self.assertEquals(len(snts), 8)

    def test_get_snts_in_exercise(self):
        snts=get_snts_in_exercise(0)
        self.assertEquals(len(snts), 3)

    def test_get_word_and_meanings(self):
        wams=get_word_and_meanings([0, 1, 3])
        self.assertEquals(len(wams), 3)
        d=wams[0].get_display()
        self.assertTrue("steep" in d)
        self.assertTrue("陡峭" in d)

    def test_get_similar_words(self):
        wams=get_similar_words("f", limit=3)
        self.assertEquals(len(wams), 2)
        self.assertEquals(wams[0].word, "fight")
        self.assertEquals(wams[1].word, "flow")

    def test_add_word_and_meaning(self):
        wam=WordAndMeaning(None, "wind")
        wam.add_meaning("n", "風")
        wam.add_meaning("v", "緾繞")
        id=add_word_and_meaning(wam)
        self.assertEquals(id, 21)
        wams2=get_word_and_meanings([21])
        self.assertEquals(len(wams2), 1)
        d=wams2[0].get_display()
        self.assertTrue("wind" in d)
        del_word_and_meaning(21)
        self.reset_word_seq()

    def reset_word_seq(self):
        set_word_seq(20)
