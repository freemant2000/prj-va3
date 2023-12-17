from vocabassistant3.sprint import parse_exec_draft
from .db_base import open_session
from .console_utils import get_lines_until_empty
from .sprint import get_sprint, parse_exec_draft, refine_exec_draft, show_exec_draft

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
