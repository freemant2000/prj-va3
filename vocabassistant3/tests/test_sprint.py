from unittest import TestCase
from datetime import date
from vocabassistant3.db_base import open_session
from vocabassistant3.sprint import get_sprint, get_exec, load_exec_draft, refine_exec_draft

class TestSpring(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()

    def test_get_sprint(self):
        sp=get_sprint(self.s, 0)
        self.assertEquals(sp.start_dt, date(2023, 12, 4))
        self.assertEquals(len(sp.execs), 2)
        self.assertEquals(sp.execs[0].dt, date(2023, 12, 4))
        self.assertEquals(len(sp.execs[0].ews), 8)
        self.assertEquals(sp.execs[1].dt, date(2023, 12, 5))
        total=sum(len(p.get_bws()) for p in sp.pracs)
        self.assertEquals(total, 18)

    def test_find_bank_words(self):
        sp=get_sprint(self.s, 0)
        bws=sp.find_bank_words("valley")
        self.assertEquals(len(bws), 1)
        bws=sp.find_bank_words("wise")
        self.assertEquals(len(bws), 1)
        bws=sp.find_bank_words("river")
        self.assertEquals(len(bws), 0)

    def test_get_exercise(self):
        e=get_exec(self.s, 0)
        self.assertEquals(len(e.ews), 8)
        self.assertEquals(len(e.snts), 3)

    def test_load_exec_draft(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft.txt")
        self.assertEquals(len(ed.words), 7)
        self.assertEquals(len(ed.sds), 3)

    def test_refine_exec_draft_wu(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft.txt")
        sp=get_sprint(self.s, 0)
        refine_exec_draft(self.s, sp, ed)
        self.assertEquals(len(ed.wus), 6)
        wu=ed.wus["squirrel"]
        self.assertEquals(wu.wd.id, 4)
        self.assertEquals(wu.m_indice, "0")

    def test_refine_exec_draft_snt_cands(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft2.txt")
        sp=get_sprint(self.s, 0)
        refine_exec_draft(self.s, sp, ed)
        self.assertEquals(len(ed.snt_cands), 3)

    def test_refine_exec_draft_extra_kw(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft2.txt")
        sp=get_sprint(self.s, 0)
        refine_exec_draft(self.s, sp, ed)
        self.assertEquals(len(ed.extra_kws), 2)
        self.assertEquals(ed.extra_kws[0], "trunk")
        self.assertEquals(ed.extra_kws[1], "dead")
