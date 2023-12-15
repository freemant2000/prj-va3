from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.students import get_student

class TestStudent(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_get_student(self):
        stu=get_student(self.s, 0)
        self.assertEquals(stu.name, "Jodie")
        self.assertEquals(len(stu.pracs), 2)

