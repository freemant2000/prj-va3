from .db_base import open_session
from .console_utils import get_lines_until_empty
from .sprint import Sprint, get_exec, get_sprint, parse_exec_draft, refine_exec_draft, show_exec_draft, show_sprint

def refine_exec_draft_tui():
    with open_session() as s:
        sp=get_sprint(s, 0)
    while True:
        print("Paste a new exercise: words, ====, then sentences")
        try:
            lines=get_lines_until_empty()
            ed=parse_exec_draft(lines)
            with open_session() as s:
                refine_exec_draft(s, sp, ed)
                show_exec_draft(ed)
        except Exception as e:
            print(str(e))

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
            