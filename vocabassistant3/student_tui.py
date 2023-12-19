from .db_base import open_session
from .practice import Practice, get_student, Student
from .sprint import get_sprints_for, show_sprint

def show_student_tui():
    stu_id=int(input("Input student ID: "))
    with open_session() as s:
        stu=get_student(s, stu_id)
        show_student(stu)

def show_student(stud: Student):
    print(f"Student {stud.id} {stud.name}")
    print("Practices")
    for prac in stud.pracs:
        show_practice(prac)

def show_practice(prac: Practice):
    print(f"{prac.id} {prac.wb.name} {prac.fr_idx}-{prac.to_idx} {prac.get_no_words()} words {prac.assess_dt}")



def student_sprints_tui():
    stu_id=input("Input student ID: ")
    with open_session() as s:
        sps=get_sprints_for(s, stu_id)
        print("Sprints")
        for sp in sps:
            show_sprint(sp)
