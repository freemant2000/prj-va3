from unittest import TestCase
from vocabassistant3.word_def import WordDef

class TestWordAndMeaning(TestCase):
    def test_display(self):
        wd=WordDef(id=0, word="hand")
        wd.add_meaning("n", "手")
        wd.add_meaning("v", "遞給")
        self.assertEquals(wd.get_display(), "hand\t手(n)、遞給(v)")
      
