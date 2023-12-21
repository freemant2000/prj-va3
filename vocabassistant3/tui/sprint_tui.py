from datetime import date
from ..console_utils import indent_pr
from ..cmd_handler import CmdHandler, ExitException
from ..practice import Practice
from ..db_base import open_session
from ..sprint import Sprint, add_sprint, get_revision_dates, get_sprint
from .exercise_tui import add_exec_draft_tui, refine_exec_draft_tui, show_exec, show_exec_summary

def add_sprint_tui(stu_id: int):
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

def sprint_main_tui():
    global sp_id
    sp_id=int(input("Input a Sprint ID: "))
    with open_session() as s:
        sp=get_sprint(s, sp_id)
    cmds={"show": ("List practices and exercises in the sprint", show_sprint_tui),
          "sum": ("Show a summary of the sprint", show_sprint_summary_tui),
          "re": ("Refine an exercise draft for the sprint", lambda: refine_exec_draft_tui(sp_id)),
          "ae": ("Add an exercise to the sprint", lambda: add_exec_draft_tui(sp_id)),
          "de": ("Delete an exercise from the sprint", del_exec_tui),          
          "del": ("Delete this sprint", del_sprint_tui),
          "mw": ("Mark the words in the sprint", mark_words_tui)}
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
        status="*" if sp.is_hard(bw) else ""
        print(f"{str(idx).ljust(3)} {(bw.wd.word+status).ljust(20)}\t{bw.wd.get_meanings()}")

def mark_words_tui():
    with open_session() as s:
        sp=get_sprint(s, sp_id)
    cmds={"sw": ("Show the words in the sprint", lambda: show_words_in_sp(sp)),
          "ch": ("Clear the hard words in the sprint", lambda: mark_hard_words(sp, False)),
          "sh": ("Set the hard words in the sprint", lambda: mark_hard_words(sp, True)),
          "save": ("Save the markings and quit", lambda: save_sp(sp))}
    ch=CmdHandler("mw>", cmds)
    ch.main_loop()

def save_sp(sp: Sprint):
    with open_session() as s:
        s.merge(sp)
        s.commit()
        print("OK")
        raise ExitException()

def mark_hard_words(sp: Sprint, hard: bool):
    indice=input("Input the indice like 0,3,7 or all: ")
    if indice=="all":
        sp.mark_all_hard(hard)
    else:
        indice=[int(idx.strip()) for idx in indice.split(",")]
        sp.mark_words_hard(indice, hard)
    print("OK")

def show_sprint_struct(sp: Sprint, pr=print):
    pr(f"Sprint {sp.id} started on {sp.start_dt}")
    pr2=indent_pr(pr)
    if sp.pracs:
        pr2(f"Practices")
        for p in sp.pracs:
            show_practice(p, pr=pr2)
    if sp.execs:
        pr2(f"Exercises")
        for idx, exec in enumerate(sp.execs):
            show_exec_summary(idx, exec, pr=pr2)

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
    for idx, exec in enumerate(sp.execs):
      show_exec(idx, exec)

def del_exec_tui():
    idx=int(input("Input the index (0 or 1, etc.) of the exercise: "))
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        exec=sp.del_exec(idx)
        s.delete(exec)
        s.commit()
        print("OK")
