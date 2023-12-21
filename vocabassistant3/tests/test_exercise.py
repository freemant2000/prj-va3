from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.sprint import add_exec_draft, get_sprint, get_exec, load_exec_draft, refine_exec_draft

class TestSprint(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()

    def test_get_exercise(self):
        e=get_exec(self.s, 1)
        self.assertEquals(len(e.ews), 8)
        self.assertEquals(len(e.snts), 3)

    def test_load_exec_draft(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft.txt")
        self.assertEquals(len(ed.words), 7)
        self.assertEquals(len(ed.sds), 3)

    def test_refine_exec_draft_wu(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft.txt")
        sp=get_sprint(self.s, 1)
        refine_exec_draft(self.s, sp, ed)
        self.assertEquals(len(ed.wus), 6)
        wu=ed.wus["squirrel"]
        self.assertEquals(wu.wd.id, 5)
        self.assertEquals(wu.m_indice, "0")

    def test_refine_exec_draft_snt_cands(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft2.txt")
        sp=get_sprint(self.s, 1)
        refine_exec_draft(self.s, sp, ed)
        self.assertEquals(len(ed.snt_cands), 3)

    def test_refine_exec_draft_extra_kw(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft2.txt")
        sp=get_sprint(self.s, 1)
        refine_exec_draft(self.s, sp, ed)
        self.assertEquals(len(ed.extra_kws), 2)
        self.assertEquals(ed.extra_kws[0], "trunk")
        self.assertEquals(ed.extra_kws[1], "dead")

    def test_save_exec_draft(self):
        ed=load_exec_draft("vocabassistant3/tests/test_exec_draft3.txt")
        self.s.begin()
        sp=get_sprint(self.s, 1)
        add_exec_draft(self.s, sp, ed)
        self.s.flush()
        exec=get_exec(self.s, 3)
        self.assertEquals(len(exec.ews), 3)
        self.assertEquals(len(exec.snts), 2)
        self.s.rollback()
        self.reset_seq()

    def reset_seq(self):
        set_seq_val(self.s, "exercises")
        set_seq_val(self.s, "sentences")
