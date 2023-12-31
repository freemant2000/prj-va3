from unittest import TestCase
from test_db_connector import open_session
from vocabassistant3.teacher import get_teacher, get_teacher_by_email

class TestTeacher(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_get_teacher(self):
        tch=get_teacher(self.s, 1)
        self.assertEquals(tch.gmail, "kent.tong.mo@gmail.com")
        self.assertEquals(len(tch.stus), 2)
    def test_get_teacher_by_email(self):
        tch=get_teacher_by_email(self.s, "kent.tong.mo@gmail.com")
        self.assertEquals(tch.id, 1)
