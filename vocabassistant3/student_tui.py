from typing import Sequence
from vocabassistant3.console_utils import indent_pr

from vocabassistant3.sprint_tui import show_sprint_struct
from .db_base import open_session
from .practice import Practice, get_student, Student
from .sprint import Sprint, get_sprints_for

def show_student_tui():
    stu_id=int(input("Input student ID: "))
    with open_session() as s:
        stu=get_student(s, stu_id)
        sps=get_sprints_for(s, stu.id)
        show_student(stu, sps)

def show_student(stud: Student, sps: Sequence[Sprint]):
    print(f"Student {stud.id} {stud.name}")
    pr=indent_pr(print)
    if stud.pracs:
        print("Practices")
        for prac in stud.pracs:
            show_practice(prac, pr)
    if sps:
        print("Sprints")
        for sp in sps:
            show_sprint_struct(sp, pr)

def show_practice(p: Practice, pr=print):
    pr(f"{p.id} {p.wb.name} {p.fr_idx}-{p.to_idx} {p.get_no_words()} {p.hard_only} {p.assess_dt}")
