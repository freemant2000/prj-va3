from unittest import TestCase
from datetime import date
from vocabassistant3.db_base import open_session
from vocabassistant3.sprint import get_revision_dates, get_sprint

class TestSprint(TestCase):
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

    def test_get_bank_words(self):
        sp=get_sprint(self.s, 0)
        bws=sp.get_bws()
        self.assertEquals(len(bws), 18)

    def test_get_revision_dates(self):
        rds=get_revision_dates(self.s, 0)
        for ew, ds in rds.items():
            if ew.wd_id==0 and ew.m_indice=="0" or \
               ew.wd_id==2 and ew.m_indice=="0":
                self.assertEquals(len(ds), 2)
            elif ew.wd_id==1 and ew.m_indice=="0":
                self.assertEquals(len(ds), 1)
        