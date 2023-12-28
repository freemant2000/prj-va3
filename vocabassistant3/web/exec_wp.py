import justpy as jp
from starlette.requests import Request
from ..buf_print import buf_pr
from ..db_base import open_session
from ..sprint import Exercise, get_exec

@jp.SetRoute("/execs/{e_id:int}")
def exec_wp(r: Request):
    e_id=int(r.path_params["e_id"])
    wp=jp.WebPage()
    try:
        with open_session() as s:
            sp=get_exec(s, e_id)
            if sp:
                buf_cnt=show_exec_buf(sp)
                jp.Textarea(value=buf_cnt, readonly=True, rows=buf_cnt.count("\n"), cols=80, style="font-family: monospace;", a=wp)
            else:
                raise ValueError(f"Exercise {e_id} not found")
    except Exception as e:
        jp.H3(text="Error: "+str(e), a=wp)
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

