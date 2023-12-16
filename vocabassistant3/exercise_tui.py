from .db_base import open_session
from .console_utils import get_lines_until_empty
from .sentence import parse_snt_draft, refine_snt_draft, show_snt_draft

def refine_exec_draft_tui():
    while True:
        print("Paste a new exercise: words, ====, then sentences")
        try:
            lines=get_lines_until_empty()
            sd=parse_snt_draft(lines)
            with open_session() as s:
                refine_snt_draft(s, sd)
            show_snt_draft(sd)
        except Exception as e:
            print(str(e))
