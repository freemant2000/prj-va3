from datetime import date
from .db_base import open_session
from .sprint import Sprint, get_revision_dates, get_sprint
from sqlalchemy.orm import Session

def show_sprint_tui():
    sp_id=int(input("Enter sprint ID: "))
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        show_sprint_summary(s, sp)

def show_sprint_summary(s: Session, sp: Sprint):
    print(f"Spring {sp.id} started on {sp.start_dt}")
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

