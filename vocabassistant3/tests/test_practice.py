from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.practice import add_practice, get_practice

class TestPractice(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_get_practice(self):
        p=get_practice(self.s, 0)
        self.assertEquals(p.fr_idx, 0)
        self.assertEquals(p.to_idx, 10)
        self.assertEquals(p.wb.name, "two-goats-level-2")
        self.assertEquals(len(p.hard_w_indice), 3)

    def test_add_practice(self):
        self.s.begin()
        add_practice(self.s, 1, 3, 4)
        self.s.flush()
        p=get_practice(self.s, 11)
        self.assertEquals(p.fr_idx, 3)
        self.assertEquals(p.to_idx, 4)
        self.assertEquals(p.wb.name, "fighting-goats-and-jackal-level-2")
        self.reset_word_seq() # seq is done outside transaction
        self.s.rollback()

    def reset_word_seq(self):
        set_seq_val(self.s, "practice_seq", 10)
