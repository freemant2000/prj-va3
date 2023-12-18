from unittest import TestCase
from vocabassistant3.db_base import open_session
from vocabassistant3.teacher import get_teacher

class TestPractice(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()

    def test_get_teacher(self):
        tch=get_teacher(self.s, 0)
        self.assertEquals(tch.gmail, "kent.tong.mo@gmail.com")
        self.assertEquals(len(tch.stus), 2)