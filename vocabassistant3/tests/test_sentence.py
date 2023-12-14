from unittest import TestCase
from vocabassistant3.db_base import open_session
from vocabassistant3.sentence import get_snts

class TestWordBank(TestCase):
    def setUp(self) -> None:
        self.s=open_session()
    def tearDown(self) -> None:
        self.s.close()
    def test_find_snts(self):
        snts=get_snts(self.s, ["squirrel", "river", "trunk"])
        self.assertEquals(len(snts), 4)
        self.assertEquals(snts[0].text, "這條河裡的水在快速地流動。")

