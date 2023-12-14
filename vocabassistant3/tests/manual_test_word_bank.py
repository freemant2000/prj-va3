from vocabassistant3.word_bank import *
from vocabassistant3.db_base import open_session

with open_session() as s:
  wbd=load_wb_input()
  show_wb_draft(wbd)
  #check_wb_draft(s, wbd)