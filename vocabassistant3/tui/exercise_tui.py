from .console_utils import get_lines_until_empty
from .sentence_tui import show_snt_draft
from ..db_base import open_session
from ..sprint import Exercise, ExerciseDraft, Sprint, add_exec_draft, get_exec, get_sprint, parse_exec_draft, refine_exec_draft

def input_exec_draft()->ExerciseDraft:
    print("Paste a new exercise: words, ====, then sentences")
    lines=get_lines_until_empty()
    ed=parse_exec_draft(lines)
    return ed

def refine_exec_draft_tui(sp_id):
    ed=input_exec_draft()
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        refine_exec_draft(s, sp, ed)
        show_exec_draft(ed, sp)

def add_exec_draft_tui(sp_id):
    ed=input_exec_draft()
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        add_exec_draft(s, sp, ed)
        s.commit()
        print("OK")

def show_exec_tui(sp_id: int):
    e_idx_str=input("Input the index (0 or 1, Enter for last) of the exercise: ")
    with open_session() as s:
        sp=get_sprint(s, sp_id)
        if e_idx_str:
            e_idx=int(e_idx_str)
        else:
            e_idx=len(sp.execs)-1
        if 0<=e_idx<len(sp.execs):
            exec=sp.execs[e_idx]
            for ew in exec.ews:
                fw=ew.get_full_word()
                print(f"{fw.ljust(20)}{ew.get_meanings()}")
            print("==========")
            for snt in exec.snts:
                print(snt.text)
            print(f"https://kenttong.pythonanywhere.com/execs/pub/{exec.id}")
        else:
            raise ValueError(f"Invalid index {e_idx}")

def show_exec_html():
    e_id=str(input("Enter exercise ID: "))
    with open_session() as s:
        exec=get_exec(s, e_id)
        html="<div>"
        html+="<h4 style='margin-bottom: 5px;'>默字</h4>"
        html+="<div style='width: 300px;'>"
        for ew in exec.ews:
            ew_html=f"""
            <div style="display: flex; width: 100%">
            <span>{ew.wd.word}</span><span style="flex-grow: 1"></span><span>{ew.wd.get_meanings()}</span>
            </div>
            """
            html+=ew_html
        html+="</div>"
        html+="<h4 style='margin-bottom: 5px;'>翻譯</h4>"
        for snt in exec.snts:
            html+=f"<div>{snt.text}</div>"
    html+="</div>"
    print(html)

def show_exec(idx: int, exec: Exercise):
    print(f"{idx} Exercise created on {exec.dt}")
    for ew in exec.ews:
        print("\t"+ew.wd.word)
    for snt in exec.snts:
        print("\t"+snt.text)
    
def show_exec_summary(idx: int, exec: Exercise, pr=print):
    pr(f"{idx} Exercise created on {exec.dt} {len(exec.ews)} words")

def show_exec_draft(ed: ExerciseDraft, sp: Sprint):
    for word in ed.words:
        if word in ed.wus:
            wu=ed.wus[word]
            print(f"{word}<={wu.wd.id},{wu.m_indice.replace(',', '-')}")
        else:
            print(word)
    print("===========")
    for sd in ed.sds:
        show_snt_draft(sd, ed.used_sds, ed.used_l2_snt_cands)
    if ed.extra_kws:
        bws=sp.get_bws()
        all_bws=sp.get_all_bws()
        print("\nExtra keywords used in the sentences")
        for kw in ed.extra_kws:
            if next((bw for bw in bws if bw.wd.word==kw), None):
                status="in sprint"
            elif next((bw for bw in all_bws if bw.wd.word==kw), None):
                status="unmarked in a practice in the sprint"
            else:
                status="not in sprint"
            print(f"\t{kw} ({status})")
    print("\nAvailable sentences")
    for snt in ed.snt_cands:
        status="(used in sprint)" if snt in ed.used_snt_cands else ""
        print(f"{snt.text}<={snt.id} {status}")

