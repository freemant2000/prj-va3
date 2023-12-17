from sqlalchemy.orm import Session
from .db_base import open_session
from .practice import get_student, Student, show_practice, show_student
from .sprint import get_sprints_for, show_sprint

def student_tui():
    stu_id=input("Input student ID: ")
    with open_session() as s:
        stu=get_student(s, stu_id)
        show_student(stu)

def student_sprints_tui():
    stu_id=input("Input student ID: ")
    with open_session() as s:
        sps=get_sprints_for(s, stu_id)
        print("Sprints")
        for sp in sps:
            show_sprint(sp)
