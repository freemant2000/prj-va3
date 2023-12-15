from vocabassistant3.practice import add_practice
from vocabassistant3.db_base import open_session

with open_session() as s:
  add_practice(s, 0, 2, 5)
