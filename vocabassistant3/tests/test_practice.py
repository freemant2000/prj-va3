from unittest import TestCase
from vocabassistant3.db_base import open_session, set_seq_val
from vocabassistant3.practice import Practice, PracticeHard, add_practice, get_practice, get_student

class TestPractice(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_no_words(self):
        p=Practice(fr_idx=1, to_idx=5)
        p.hard_w_indice.append(PracticeHard(w_idx=2))
        p.hard_w_indice.append(PracticeHard(w_idx=3))
        p.hard_w_indice.append(PracticeHard(w_idx=5))
        self.assertEquals(p.get_no_words(), 5)
        p.hard_only=True
        self.assertEquals(p.get_no_words(), 3)

    def test_get_words(self):
       p=get_practice(self.s, 0)
       bws=p.get_bws()
       self.assertEquals(len(bws), 11)
       p.hard_only=True
       bws=p.get_bws()
       self.assertEquals(len(bws), 3)
       self.assertEquals(bws[0].wd_id, 1)

    def test_find_bank_words(self):
       p=get_practice(self.s, 0)
       bws=p.find_bank_words("valley")
       self.assertEquals(len(bws), 1)
       bws=p.find_bank_words("wise")
       self.assertEquals(len(bws), 0)

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

    def test_get_student(self):
        stu=get_student(self.s, 0)
        self.assertEquals(stu.name, "Jodie")
        self.assertEquals(len(stu.pracs), 2)