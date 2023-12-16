from vocabassistant3.word_bank import *
from vocabassistant3.db_base import open_session

with open_session() as s:
  wbd=load_wb_input("vocabassistant3/tests/test_wb_input.txt")
  refine_wb_draft(s, wbd)
  show_wb_draft(wbd)
