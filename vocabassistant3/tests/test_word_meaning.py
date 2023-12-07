from unittest import TestCase
from vocabassistant3.word_meaning import *

class TestWordAndMeaning(TestCase):
    def test_display(self):
        wam=WordAndMeaning("hand")
        wam.add_meaning("n", "手")
        wam.add_meaning("v", "遞給")
        self.assertEquals(wam.get_display(), "hand\t手(n)、遞給(v)")
      