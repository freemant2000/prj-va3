from flask import request, redirect, render_template
from ..teacher import get_teacher
from ..sprint import Exercise, Sprint, get_sprints_for
from ..buf_print import buf_pr, indent_pr
from ..db_base import open_session
from ..practice import Practice, get_student
from .user_prod_flask import get_current_user

def stud_main_wp(stu_id):
    try:
        tch_id=get_current_user()
        if not tch_id:
            return redirect("/login")
        with open_session() as s:
            tch=get_teacher(s, tch_id)
            stu=get_student(s, stu_id)
            if not stu:
                raise ValueError(f"Student {stu_id} not found")
            if not tch.teaches(stu):
                raise ValueError(f"You are teaching that student")
            sps=get_sprints_for(s, stu_id)
            buf_cnt=show_stu_buf(stu, sps)
            return render_template("stud_wp.html", 
                                   ta_cnt=buf_cnt, 
                                   rows=buf_cnt.count("\n"),
                                   sps=sps)
    except Exception as e:
        return "Error: "+str(e)

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
