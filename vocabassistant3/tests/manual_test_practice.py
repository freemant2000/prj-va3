from vocabassistant3.practice import add_practice, get_student, show_student
from vocabassistant3.db_base import open_session

with open_session() as s:
  #add_practice(s, 0, 2, 5)
  stud=get_student(s, 0)
  show_student(stud)

