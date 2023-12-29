import justpy as jp
from starlette.requests import Request
from .user_prod_web import get_current_user
from ..sprint import Exercise, Sprint, get_sprints_for
from ..buf_print import buf_pr, indent_pr
from ..db_base import open_session
from ..practice import Practice, get_student

@jp.SetRoute("/stus/{stu_id:int}")
def stud_main_wp(r: Request):
    wp=jp.WebPage()
    wp.err=jp.P(text="", a=wp)
    try:
        tch=get_current_user(r.session_id)
        if not tch:
            wp.redirect="/login"
            return wp
        stu_id=int(r.path_params["stu_id"])
        with open_session() as s:
            stu=get_student(s, stu_id)
            if not stu:
                raise ValueError(f"Student {stu_id} not found")
            tch.check_teaches(sp.stu)
            sps=get_sprints_for(s, stu_id)
            buf_cnt=show_stu_buf(stu, sps)
            jp.Textarea(value=buf_cnt, rows=buf_cnt.count("\n"), cols=80, style="font-family: monospace;", a=wp)
            sps_ul=jp.Ul(a=wp)
            for sp in sps:
                sp_li=jp.Li(a=sps_ul)
                jp.A(text=f"Sprint {sp.id}", href=f"../sprints/{sp.id}", a=sp_li)
    except Exception as e:
        wp.err.text="Error: "+str(e)
    return wp

def show_stu_buf(stu, sps)->str:
    buf, pr=buf_pr()
    pr2=indent_pr(pr)
    if stu.pracs:
        pr("Practices")
        for prac in stu.pracs:
            show_practice(prac, pr2)
    if sps:
        print("Sprints")
        for sp in sps:
            show_sprint_struct(sp, pr2)
    return buf.getvalue()

def show_practice(p: Practice, pr):
    h_wc, all_wc=p.get_word_counts()
    pr(f"{p.id} {p.wb.name} {p.fr_idx}-{p.to_idx} {h_wc}/{all_wc} {p.hard_only} {p.assess_dt}")

def show_sprint_struct(sp: Sprint, pr):
    pr(f"Sprint {sp.id} started on {sp.start_dt}")
    pr2=indent_pr(pr)
    if sp.pracs:
        pr2(f"Practices")
        for p in sp.pracs:
            show_practice(p, pr2)
    if sp.execs:
        pr2(f"Exercises")
        for idx, exec in enumerate(sp.execs):
            show_exec_summary(idx, exec, pr2)

def show_exec_summary(idx: int, exec: Exercise, pr):
    pr(f"{idx} Exercise created on {exec.dt} {len(exec.ews)} words")
