from .sentence_tui import show_snt_draft
from .sentence import get_snt, get_snts_from_keywords, refine_snt_draft
from .word_def import WordUsage
from .db_base import open_session
from .console_utils import get_lines_until_empty
from .sprint import Exercise, ExerciseDraft, Sprint, get_exec, get_sprint, parse_exec_draft
from sqlalchemy.orm import Session

def refine_exec_draft_tui(sp_id):
    print("Paste a new exercise: words, ====, then sentences")
    with open_session() as s:
        lines=get_lines_until_empty()
        ed=parse_exec_draft(lines)
        sp=get_sprint(s, sp_id)
        refine_exec_draft(s, sp, ed)
        show_exec_draft(ed, sp)

def add_exec_draft_tui(sp_id):
    pass

# def init_exec_draft_tui():
#     with open_session() as s:
#         sp=get_sprint(s, 0)
#         show_sprint_for_new_exec(sp)
#         print("Paste a new exercise: words, ====, then sentences")
#         try:
#             lines=get_lines_until_empty()
#             ed=parse_exec_draft(lines)
#             with open_session() as s:
#                 refine_exec_draft(s, sp, ed)
#                 show_exec_draft(ed)
#         except Exception as e:
#             print(str(e))

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

def show_exec(exec: Exercise):
    print(f"Exercise {exec.id} created on {exec.dt}")
    for ew in exec.ews:
        print("\t"+ew.wd.word)
    for snt in exec.snts:
        print("\t"+snt.text)
    
def show_exec_summary(exec: Exercise, pr=print):
    pr(f"Exercise {exec.id} created on {exec.dt} {len(exec.ews)} words")

def show_exec_draft(ed: ExerciseDraft, sp: Sprint):
    for word in ed.words:
        if word in ed.wus:
            wu=ed.wus[word]
            print(f"{word}<={wu.wd.id},{wu.m_indice.replace(',', '-')}")
        else:
            print(word)
    print("===========")
    for sd in ed.sds:
        show_snt_draft(sd)
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
        print(f"{snt.text}<={snt.id}")

def refine_exec_draft(s: Session, sp: Sprint, ed: ExerciseDraft):
    for word in ed.words:
        if not (word in ed.wus):
            bws=sp.find_bank_words(word)
            if bws:
                wu=WordUsage(wd=bws[0].wd, m_indice=bws[0].m_indice)
                ed.wus[word]=wu
    for sd in ed.sds:
        refine_snt_draft(s, sd)
    ed.snt_cands=[t[0] for t in get_snts_from_keywords(s, ed.words)]
    ed.extra_kws.clear()
    for sd in ed.sds:
        if sd.snt_id!=None:
            snt=get_snt(s, sd.snt_id)
            for wm in snt.keywords:
                if wm.wd.word not in ed.words:
                    ed.extra_kws.append(wm.wd.word)
        else:
            for kw in sd.keywords:
                if kw not in ed.words:
                    ed.extra_kws.append(kw)

