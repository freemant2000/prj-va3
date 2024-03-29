from unittest import TestCase
from datetime import date
from test_db_connector import open_session
from vocabassistant3.db_base import set_seq_val
from vocabassistant3.practice import get_practice
from vocabassistant3.sentence import Sentence
from vocabassistant3.sprint import add_sprint, get_revision_dates, get_sprint, get_sprint_for_exec

class TestSprint(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()

    def test_get_sprint(self):
        sp=get_sprint(self.s, 1)
        self.assertEquals(sp.start_dt, date(2023, 12, 4))
        self.assertEquals(len(sp.execs), 2)
        self.assertEquals(sp.execs[0].dt, date(2023, 12, 4))
        self.assertEquals(len(sp.execs[0].ews), 8)
        self.assertEquals(sp.execs[1].dt, date(2023, 12, 5))
        total=sum(len(p.get_bws()) for p in sp.pracs)
        self.assertEquals(total, 18)

    def test_add_sprint(self):
        sp=add_sprint(self.s, 1, [2])
        self.assertEquals(len(sp.pracs), 1)
        self.s.flush()
        sp2=get_sprint(self.s, 2)
        self.assertEquals(len(sp2.pracs), 1)
        self.assertEquals(sp2.pracs[0].id, 2)
        self.assertEquals(len(sp2.execs), 0)
        self.s.rollback()
        self.reset_seq()

    def test_find_bank_words(self):
        sp=get_sprint(self.s, 1)
        bws=sp.find_bank_words("valley")
        self.assertEquals(len(bws), 1)
        bws=sp.find_bank_words("wise")
        self.assertEquals(len(bws), 1)
        bws=sp.find_bank_words("river")
        self.assertEquals(len(bws), 0)

    def test_get_bank_words(self):
        sp=get_sprint(self.s, 1)
        bws=sp.get_bws()
        self.assertEquals(len(bws), 18)

    def test_get_revision_dates(self):
        rds=get_revision_dates(self.s, 1)
        for ew, ds in rds.items():
            if ew.wd_id==1 and ew.m_indice=="0" or \
               ew.wd_id==3 and ew.m_indice=="0":
                self.assertEquals(len(ds), 2)
            elif ew.wd_id==1 and ew.m_indice=="0":
                self.assertEquals(len(ds), 1)

    def test_mark_as_hard(self):
       self.s.begin()
       sp=get_sprint(self.s, 1)
       sp.clear_hard()
       sp.mark_words_hard([2, 12])
       self.s.flush()
       p=get_practice(self.s, 2)
       self.assertEquals(len(p.hard_w_indice), 1)
       self.assertEquals(p.hard_w_indice[0].w_idx, 1)
       self.s.rollback()

    def test_contains_prac(self):
       sp=get_sprint(self.s, 1)
       self.assertTrue(sp.contains_prac(get_practice(self.s, 2)))
       self.assertFalse(sp.contains_prac(get_practice(self.s, 3)))

    def test_add_prac(self):
       self.s.begin()
       sp=get_sprint(self.s, 1)
       prac=get_practice(self.s, 3)
       sp.add_prac(prac)
       self.s.flush()
       sp2=get_sprint(self.s, 1)
       self.assertTrue(sp2.contains_prac(prac))
       self.s.rollback()

    def test_del_prac(self):
       self.s.begin()
       sp=get_sprint(self.s, 1)
       sp.del_prac(2)
       self.s.flush()
       sp2=get_sprint(self.s, 1)
       self.assertEquals(len(sp2.pracs), 1)
       self.assertEquals(sp2.pracs[0].id, 1)
       self.s.rollback()

    def test_uses_snt(self):
       sp=get_sprint(self.s, 1)
       self.assertTrue(sp.uses_snt(Sentence(id=1)))
       self.assertTrue(sp.uses_snt(Sentence(id=6)))
       self.assertFalse(sp.uses_snt(Sentence(id=7)))

    def test_get_sprint_for_exec(self):
       sp=get_sprint_for_exec(self.s, 2)
       self.assertEquals(sp.id, 1)

    def reset_seq(self):
        set_seq_val(self.s, "sprints")
       
