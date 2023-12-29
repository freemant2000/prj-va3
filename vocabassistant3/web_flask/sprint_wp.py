from flask import redirect, render_template
from datetime import date
from sqlalchemy.orm import Session
from ..teacher import get_teacher
from .user_prod_flask import get_current_user
from ..buf_print import buf_pr
from ..db_base import open_session
from ..sprint import get_revision_dates, get_sprint

def sprint_wp(sp_id):
    try:
        tch_id=get_current_user()
        if not tch_id:
            return redirect("/login")
        with open_session() as s:
            tch=get_teacher(s, tch_id)
            sp=get_sprint(s, sp_id)
            if sp:
                tch.check_teaches(sp.stu)
                buf_cnt=show_sprint_buf(s, sp)
                return render_template("sprint_wp.html", 
                                    ta_cnt=buf_cnt, 
                                    rows=int(1.5*buf_cnt.count("\n")),
                                    execs=sp.execs)
            else:
                raise ValueError(f"Sprint {sp_id} not found")
    except Exception as e:
        return "Error: "+str(e)

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

