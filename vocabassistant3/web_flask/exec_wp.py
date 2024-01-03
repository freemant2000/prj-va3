from flask import request, redirect, render_template
from ..teacher import get_teacher
from .user_prod_flask import get_current_user
from ..buf_print import buf_pr
from ..db_base import open_session
from ..sprint import Exercise, get_exec, get_sprint_for_exec

def exec_wp(e_id):
    try:
        tch_id=get_current_user()
        if not tch_id:
            return redirect("/login")
        with open_session() as s:
            tch=get_teacher(s, tch_id)
            sp=get_sprint_for_exec(s, e_id)
            if not sp:
                raise ValueError(f"No sprint contains that exercise")
            tch.check_teaches(sp.stu)
            exec=get_exec(s, e_id)
            if not exec:
                raise ValueError(f"Exercise {e_id} not found")
            buf_cnt=show_exec_buf(exec)
            return render_template("exec_wp.html", 
                                   ta_cnt=buf_cnt, 
                                   rows=int(1.5*buf_cnt.count("\n")))
    except Exception as e:
        return "Error: "+str(e)

def show_exec_buf(exec: Exercise)->str:
    buf, pr=buf_pr()
    pr(f"Exercise created on {exec.dt}")
    for ew in exec.ews:
        fw=ew.get_full_word()
        pr(f"{fw.ljust(20)}{ew.get_meanings()}")
    pr("============")
    for snt in exec.snts:
        pr(snt.text)
    return buf.getvalue()

