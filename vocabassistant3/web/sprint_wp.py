from datetime import date
from io import StringIO
import justpy as jp
from starlette.requests import Request
from sqlalchemy.orm import Session
from ..buf_print import buf_pr
from ..db_base import open_session
from ..sprint import get_revision_dates, get_sprint

@jp.SetRoute("/sprints/{sp_id:int}")
def sprint_wp(r: Request):
    sp_id=int(r.path_params["sp_id"])
    wp=jp.WebPage()
    try:
        with open_session() as s:
            sp=get_sprint(s, sp_id)
            if sp:
                buf_cnt=show_sprint_buf(s, sp)
                jp.Textarea(value=buf_cnt, rows=buf_cnt.count("\n"), cols=80, style="font-family: monospace;", a=wp)
                execs_ul=jp.Ul(a=wp)
                for exec in sp.execs:
                    exec_li=jp.Li(a=execs_ul)
                    jp.A(text=f"Exercise {exec.id}", href=f"../execs/{exec.id}", a=exec_li)
            else:
                raise ValueError(f"Sprint {sp_id} not found")
    except Exception as e:
        jp.H3(text="Error: "+str(e), a=wp)
    return wp

def show_sprint_buf(s: Session, sp)->str:
    buf, pr=buf_pr()
    pr(f"Sprint {sp.id} started on {sp.start_dt}")
    pr("Revision summary")
    today=date.today()
    rds=get_revision_dates(s, sp.id)
    wd_ds={ew.wd: ds for (ew, ds) in rds.items()}
    for idx, bw in enumerate(sp.get_bws()):
        if bw.wd in wd_ds:
            ds=wd_ds.get(bw.wd)
            days=[str((today-d).days) for d in ds]
            days=",".join(days)
            rev_info=f"{days} day(s) ago"
        else:
            rev_info=""
        fw=bw.get_full_word()
        pr(f"{str(idx).ljust(3)} {fw.ljust(20)}\t{bw.wd.get_meanings()}\t{rev_info}")
    pr("Sentences used")
    for snt in (s for exec in sp.execs for s in exec.snts):
        pr(snt.text)
    return buf.getvalue()

