from vocabassistant3.db_base import open_session
from vocabassistant3.sprint import get_sprint, show_sprint

with open_session() as s:
  sp=get_sprint(s, 0)
  show_sprint(sp)
  
