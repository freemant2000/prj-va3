from unittest import TestCase
from vocabassistant3.models import *

class TestWordAndMeaning(TestCase):
    def test_display(self):
        wam=WordAndMeaning(0, "can")
        wam.add_meaning("n", "罐")
        wam.add_meaning("m", "能夠")
        self.assertEquals(wam.get_display(), "can\t罐(n)、能夠(m)")
   