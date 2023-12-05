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
