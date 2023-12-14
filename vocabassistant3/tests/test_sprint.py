from unittest import TestCase
from datetime import date
from vocabassistant3.db_base import open_session
from vocabassistant3.sprint import get_sprint, get_exec

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

    def test_get_exercise(self):
        e=get_exec(self.s, 0)
        self.assertEquals(len(e.ews), 8)
        self.assertEquals(len(e.snts), 3)

