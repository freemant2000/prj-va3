from datetime import date
from glob import glob

from vocabassistant3.console_utils import indent_pr
from .cmd_handler import CmdHandler
from .practice import Practice
from .exercise_tui import add_exec_draft_tui, refine_exec_draft_tui, show_exec, show_exec_summary
from .db_base import open_session
from .sprint import Sprint, add_sprint, get_revision_dates, get_sprint, get_sprints_for
from sqlalchemy.orm import Session

stu_id: int=None
sp_id: int=None

def sprints_tui(s_id: int):
    global stu_id
    stu_id=s_id
    cmds={"show": ("List all the sprints for the student", show_sprints_tui),
          "add": ("Add a sprint", lambda: make_sprint_tui(stu_id)),
          "del": ("Delete a sprint", del_sprint_tui),
          "sp": ("Work on a sprint", sprint_tui)}
    ch=CmdHandler("sps>", cmds)
    ch.main_loop()

def make_sprint_tui(stu_id: int):
    p_ids=[int(p_id) for p_id in input("Input one or more practice IDs like 2,4,5: ").split(",")]
    with open_session() as s:
        add_sprint(s, stu_id, p_ids)
        s.commit()
        print("OK")

def del_sprint_tui():
    sp_id=int(input("Input the Sprint ID: "))
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        if sp:
            s.delete(sp)
            s.commit()
            print("OK")
        else:
            print(f"Sprint {sp_id} not found")

def show_sprints_tui():
    with open_session() as s:
        sps=get_sprints_for(s, stu_id)
        for sp in sps:
            show_sprint_struct(sp)

def sprint_tui():
    global sp_id
    sp_id=int(input("Input a Sprint ID: "))
    with open_session() as s:
        sp=get_sprint(s, sp_id)
    cmds={"show": ("List practices and exercises in the sprint", show_sprint_tui),
          "sum": ("Show a summary of the sprint", show_sprint_summary_tui),
          "re": ("Refine an exercise draft for the sprint", lambda: refine_exec_draft_tui(sp_id)),
          "ae": ("Add an exercise to the sprint", lambda: add_exec_draft_tui(sp_id)),
          "del": ("Delete this sprint", del_sprint_tui),
          "sw": ("Show all the words in the sprint", show_words_tui),
          "ch": ("Clear all the hard words in the sprint", None),
          "sh": ("Set the hard words in the sprint", None),}
    ch=CmdHandler("sp>", cmds)
    ch.main_loop()

def show_sprint_tui():
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        show_sprint_struct(sp)

def show_words_tui():
    with open_session() as s:
        sp=get_sprint(s, sp_id)
    show_words_in_sp(sp)

def show_words_in_sp(sp: Sprint):
    for idx, bw in enumerate(sp.get_bws()):
        print(f"{str(idx).ljust(3)} {bw.wd.word.ljust(20)}\t{bw.wd.get_meanings()}")

def show_sprint_struct(sp: Sprint, pr=print):
    pr(f"Sprint {sp.id} started on {sp.start_dt}")
    pr2=indent_pr(pr)
    if sp.pracs:
        pr2(f"Practices")
        for p in sp.pracs:
            show_practice(p, pr=pr2)
    if sp.execs:
        pr2(f"Exercises")
        for exec in sp.execs:
            show_exec_summary(exec, pr=pr2)

def show_practice(p: Practice, pr=print):
    pr(f"{p.id} {p.wb.name} {p.fr_idx}-{p.to_idx} {p.get_no_words()} {p.hard_only} {p.assess_dt}")

def show_sprint_summary_tui():
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        print(f"Sprint {sp.id} started on {sp.start_dt}")
        print("Revision summary")
        today=date.today()
        rds=get_revision_dates(s, sp.id)
        wd_ds={ew.wd: ds for (ew, ds) in rds.items()}
        for idx, bw in enumerate(sp.get_bws()):
            if bw.wd in wd_ds:
                ds=wd_ds.get(bw.wd)
                days=[str((today-d).days) for d in ds]
                days=",".join(days)
                rev_info=f"revised {days} day(s) ago"
            else:
                rev_info=""
            print(f"{str(idx).ljust(3)} {bw.wd.word.ljust(20)}\t{bw.wd.get_meanings()}\t{rev_info}")

def show_sprint_details(sp: Sprint):
    print(f"Sprint {sp.id} started on {sp.start_dt}")
    print("\nPractices")
    for p in sp.pracs:
      print(p.id, p.wb.name)
      for bw in p.get_bws():
        print("\t"+bw.wd.word)
    print("\nExercises")
    for exec in sp.execs:
      show_exec(exec)

