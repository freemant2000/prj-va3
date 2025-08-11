from unittest import TestCase
from test_db_connector import open_session
from vocabassistant3.db_base import set_seq_val
from vocabassistant3.practice import Practice, PracticeHard, add_practice, get_practice, get_student, get_student_full_assess
from vocabassistant3.word_bank import BankWord

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
       p=get_practice(self.s, 1) #bk1 0-10. hard: 1,3,8
       bws=p.get_bws()
       self.assertEquals(len(bws), 11)
       p.hard_only=True
       bws=p.get_bws()
       print(bws[0].wd_id)
       print(bws[1].wd_id)
       print(bws[2].wd_id)
       self.assertEquals(len(bws), 3)
       self.assertEquals(bws[0].wd_id, 2)

    def test_get_all_words(self):
       p=get_practice(self.s, 1)
       p.hard_only=True
       bws=p.get_all_bws()
       self.assertEquals(len(bws), 11)

    def test_mark_as_hard(self):
       self.s.begin()
       p=get_practice(self.s, 1)
       bws=p.get_bws()
       p.hard_only=True
       p.clear_hard()
       p.mark_words_hard([bws[0], bws[4]])
       self.s.flush()
       bws=p.get_bws()
       self.assertEquals(len(bws), 2)
       self.assertEquals(bws[0].wd.word, "steep")
       self.assertEquals(bws[1].wd.word, "squirrel")
       self.s.rollback()

    def test_clear_as_hard(self):
       self.s.begin()
       p=get_practice(self.s, 3)
       bws=p.get_all_bws()  #bk1 4-9, hard: 5, 6
       p.mark_words_hard([bws[2]], False) #hard: 5
       p.mark_words_hard([bws[4]], True)  #hard: 5, 8
       self.s.flush()
       bws=p.get_bws()
       self.assertEquals(len(bws), 2)
       self.assertEquals(bws[0].wd.word, "valley")
       self.assertEquals(bws[1].wd.word, "opposite")
       self.s.rollback()

    def test_is_hard(self):
       p=get_practice(self.s, 3)  #bk1 4-9, hard: 5, 6
       self.assertTrue(p.is_hard(BankWord(wd_id=6, m_indice="0")))
       self.assertTrue(p.is_hard(BankWord(wd_id=7, m_indice="0")))
       self.assertFalse(p.is_hard(BankWord(wd_id=8, m_indice="0")))

    def test_is_hard(self):
       p=get_practice(self.s, 3)  #bk1 4-9, hard: 5, 6
       p.mark_all_hard(True)
       self.assertTrue(p.is_hard(BankWord(wd_id=5, m_indice="0")))
       p.mark_all_hard(False)
       self.assertFalse(p.is_hard(BankWord(wd_id=5, m_indice="0")))

    def test_find_bank_words(self):
       p=get_practice(self.s, 1)
       bws=p.find_bank_words("valley")
       self.assertEquals(len(bws), 1)
       bws=p.find_bank_words("wise")
       self.assertEquals(len(bws), 0)

    def test_get_practice(self):
        p=get_practice(self.s, 1)
        self.assertEquals(p.fr_idx, 0)
        self.assertEquals(p.to_idx, 10)
        self.assertEquals(p.wb.name, "two-goats-level-2")
        self.assertEquals(len(p.hard_w_indice), 3)

    def test_add_practice(self):
        self.s.begin()
        add_practice(self.s, 1, 2, 3, 4)
        self.s.flush()
        p=get_practice(self.s, 4)
        self.assertEquals(p.fr_idx, 3)
        self.assertEquals(p.to_idx, 4)
        self.assertEquals(p.wb.name, "fighting-goats-and-jackal-level-2")
        self.s.rollback()
        self.reset_word_seq() # seq is done outside transaction

    def reset_word_seq(self):
        set_seq_val(self.s, "practices")

    def test_get_student(self):
        stu=get_student(self.s, 1)
        self.assertEquals(stu.name, "Jodie")
        self.assertEquals(len(stu.pracs), 2)

    def test_get_student_full_assess(self):
        stu=get_student_full_assess(self.s, 1)
        self.assertEquals(stu.name, "Jodie")
        self.assertEquals(len(stu.pracs), 2)
        self.assertEquals(len(stu.pracs.full_assess_list), 2)