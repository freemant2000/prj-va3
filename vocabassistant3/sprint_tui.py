from .db_base import open_session
from .sprint import Sprint, get_sprint

def show_sprint_tui():
    sp_id=int(input("Enter sprint ID: "))
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        show_sprint_summary(sp)

def show_sprint_summary(sp: Sprint):
    print(f"Spring {sp.id} started on {sp.start_dt}")
    print("Words")
    for bw in sp.get_bws():
        rds=sp.get_revision_dates(bw)
        print(f"\t{bw.wd.get_display()}\t{bw.m_indice}")
    
