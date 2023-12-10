from unittest import TestCase
from vocabassistant3.va3 import *
from datetime import date
from sqlalchemy import text

class TestVA3(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_find_snts(self):
        snts=get_snts(self.s, ["squirrel", "river", "trunk"])
        self.assertEquals(len(snts), 4)
        self.assertEquals(snts[0].text, "這條河裡的水在快速地流動。")

    def test_get_sprint(self):
        sp=get_sprint(self.s, 0)
        self.assertEquals(sp.start_dt, date(2023, 12, 4))
        self.assertEquals(len(sp.execs), 2)
        self.assertEquals(sp.execs[0].dt, date(2023, 12, 4))
        self.assertEquals(len(sp.execs[0].wds), 8)
        self.assertEquals(sp.execs[1].dt, date(2023, 12, 5))
        total=sum(len(p.get_wds()) for p in sp.pracs)
        self.assertEquals(total, 18)

    def test_get_exercise(self):
        e=get_exec(self.s, 0)
        self.assertEquals(len(e.wds), 8)
        self.assertEquals(len(e.snts), 3)

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

    def test_add_word_def(self):
        wd=WordDef(word="hand")
        wd.add_meaning("n", "手")
        wd.add_meaning("v", "遞給")
        self.s.add(wd)
        self.s.commit()
        self.assertEquals(wd.id, 21)
        wd2=get_word_defs(self.s, [21])
        self.assertEquals(len(wd2), 1)
        d=wd2[0].get_display()
        self.assertTrue("hand" in d)
        self.s.close()
        self.s=open_session()
        del_word_def(self.s, 21)
        self.s.commit()
        self.reset_word_seq()

    def reset_word_seq(self):
        self.s.execute(text("select setval('word_seq', 20)"))

