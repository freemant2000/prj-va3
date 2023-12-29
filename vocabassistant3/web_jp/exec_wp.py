import justpy as jp
from starlette.requests import Request
from .user_prod_web import get_current_user
from ..buf_print import buf_pr
from ..db_base import open_session
from ..sprint import Exercise, get_exec, get_sprint_for_exec

@jp.SetRoute("/execs/{e_id:int}")
def exec_wp(r: Request):
    wp=jp.WebPage()
    wp.err=jp.P(text="", a=wp)
    try:
        tch=get_current_user(r.session_id)
        if not tch:
            wp.redirect="/login"
            return wp
        e_id=int(r.path_params["e_id"])
        with open_session() as s:
            sp=get_sprint_for_exec(s, e_id)
            if not sp:
                raise ValueError(f"No sprint contains that exercise")
            tch.check_teaches(sp.stu)
            exec=get_exec(s, e_id)
            if not exec:
                raise ValueError(f"Exercise {e_id} not found")
            buf_cnt=show_exec_buf(exec)
            jp.Textarea(value=buf_cnt, readonly=True, rows=buf_cnt.count("\n"), cols=80, style="font-family: monospace;", a=wp)
    except Exception as e:
        wp.err.text="Error: "+str(e)
    return wp

def show_exec_buf(exec: Exercise)->str:
    buf, pr=buf_pr()
    pr(f"Exercise created on {exec.dt}")
    for ew in exec.ews:
        pr(f"{ew.wd.word.ljust(20)}{ew.wd.get_meanings()}")
    pr("============")
    for snt in exec.snts:
        pr(snt.text)
    return buf.getvalue()

