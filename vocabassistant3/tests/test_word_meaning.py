from unittest import TestCase
from vocabassistant3.models import *

class TestWordAndMeaning(TestCase):
    def test_display(self):
<<<<<<< HEAD
        wam=WordAndMeaning("hand")
        wam.add_meaning("n", "手")
        wam.add_meaning("v", "遞給")
        self.assertEquals(wam.get_display(), "hand\t手(n)、遞給(v)")
      
=======
        wam=WordAndMeaning(0, "can")
        wam.add_meaning("n", "罐")
        wam.add_meaning("m", "能夠")
        self.assertEquals(wam.get_display(), "can\t罐(n)、能夠(m)")
   
>>>>>>> e037aa5b74b69597642bd800cdc43dc69146f3b2
