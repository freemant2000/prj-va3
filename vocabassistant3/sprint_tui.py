from datetime import date
from .practice import Practice
from .exercise_tui import show_exec, show_exec_summary
from .db_base import open_session
from .sprint import Sprint, get_revision_dates, get_sprint
from sqlalchemy.orm import Session

def show_sprint_struct(sp: Sprint, pr=print):
    pr(f"Sprint {sp.id} started on {sp.start_dt}")
    if sp.pracs:
        pr(f"Practices")
        for p in sp.pracs:
            show_practice(p, pr=pr)
    if sp.execs:
        pr(f"Exercises")
        for exec in sp.execs:
            show_exec_summary(exec, pr=pr)

def show_practice(p: Practice, pr=print):
    pr(f"{p.id} {p.wb.name} {p.fr_idx}-{p.to_idx} {p.get_no_words()} {p.hard_only} {p.assess_dt}")

def show_sprint_summary(s: Session, sp: Sprint):
    print(f"Sprint {sp.id} started on {sp.start_dt}")
    print("Words")
    for bw in sp.get_bws():
        print(f"\t{bw.wd.get_display()}\t{bw.m_indice}")
    print("Revision summary")
    today=date.today()
    rds=get_revision_dates(s, sp.id)
    for ew, ds in rds.items():
        days=[str((today-d).days) for d in ds]
        days=",".join(days)
        print(f"\t{ew.wd.word}\trevised {days} day(s) ago")

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

