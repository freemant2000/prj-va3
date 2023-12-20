from typing import Sequence
from .cmd_handler import CmdHandler
from .console_utils import indent_pr
from .sprint_tui import show_sprint_struct
from .db_base import open_session
from .practice import Practice, get_student, Student
from .sprint import Sprint, get_sprints_for

stu_id=0

def show_student_tui():
    global stu_id
    stu_id=int(input("Input student ID: "))
    with open_session() as s:
        stu=get_student(s, stu_id)
    cmds={"show": ("List practices and sprints for the student", show_student)}
    ch=CmdHandler(f"{stu.name}>", cmds)
    ch.main_loop()

def show_student():
    with open_session() as s:
        stud=get_student(s, stu_id)
        sps=get_sprints_for(s, stu_id)
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
