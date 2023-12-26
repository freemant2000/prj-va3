from .cmd_handler import CmdHandler
from .console_utils import indent_pr
from .word_bank_search_tui import search_word_bank_tui
from .sprint_tui import del_sprint_tui, add_sprint_tui, show_sprint_struct, sprint_main_tui
from ..db_base import open_session
from ..practice import Practice, add_practice, get_practice, get_student
from ..sprint import get_sprints_for

stu_id=0

def show_student_tui():
    global stu_id
    stu_id=int(input("Input student ID: "))
    with open_session() as s:
        stu=get_student(s, stu_id)
    cmds={"show": ("List practices and sprints for the student", show_student),
          "ap": ("Add a practice for the student", add_practice_tui),
          "dp": ("Delete a practice for the student", del_practice_tui),
          "tp": ("Toggle the hard words only switch of a practice", toggle_hard_practice_tui),
          "asp": ("Add a sprint", lambda: add_sprint_tui(stu_id)),
          "dsp": ("Delete a sprint", del_sprint_tui),
          "sp": ("Work on a sprint", sprint_main_tui)}
    ch=CmdHandler(f"{stu.name}>", cmds)
    ch.main_loop()

def show_student():
    with open_session() as s:
        stu=get_student(s, stu_id)
        sps=get_sprints_for(s, stu_id)
    pr=indent_pr(print)
    if stu.pracs:
        print("Practices")
        for prac in stu.pracs:
            show_practice(prac, pr)
    if sps:
        print("Sprints")
        for sp in sps:
            show_sprint_struct(sp, pr)

def show_practice(p: Practice, pr=print):
    h_wc, all_wc=p.get_word_counts()
    pr(f"{p.id} {p.wb.name} {p.fr_idx}-{p.to_idx} {h_wc}/{all_wc} {p.hard_only} {p.assess_dt}")

def del_practice_tui():
    p_id=int(input("Input practice ID: "))
    with open_session() as s:
        prac=get_practice(s, p_id)
        if prac:
            s.delete(prac)
            s.commit()
            print("OK")
        else:
            print(f"Practice with ID {p_id} not found")

def toggle_hard_practice_tui():
    p_id=int(input("Input practice ID: "))
    with open_session() as s:
        prac=get_practice(s, p_id)
        if prac:
            prac.hard_only=not prac.hard_only
            s.commit()
            print("OK")
        else:
            print(f"Practice with ID {p_id} not found")

def add_practice_tui():
    wb=search_word_bank_tui()
    max_idx=wb.get_no_words()-1
    rs=input("Enter a word range such as 0-4 or all: ")
    if rs=="all":
        fr_idx=0
        to_idx=max_idx
    else:
        ps=rs.strip().split("-")
        if len(ps)==2:
            fr_idx=int(ps[0])
            to_idx=int(ps[1])
        else:
            raise ValueError(f"Invalid range {rs}")
    if 0<=fr_idx<=to_idx<=max_idx:
        with open_session() as s:
            add_practice(s, stu_id, wb.id, fr_idx, to_idx)
            s.commit()
            print("OK")
    else:
        raise ValueError(f"Range {fr_idx}-{to_idx} is outside 0-{max_idx}")

