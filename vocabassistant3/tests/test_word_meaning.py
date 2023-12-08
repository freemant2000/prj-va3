from unittest import TestCase
from vocabassistant3.models import *

class TestWordAndMeaning(TestCase):
    def test_display(self):
        wam=WordDef()
        wam.id=0
        wam.word="hand"
        wam.add_meaning("n", "手")
        wam.add_meaning("v", "遞給")
        self.assertEquals(wam.get_display(), "hand\t手(n)、遞給(v)")
      
