from .db_base import open_session
from .console_utils import get_lines_until_empty
from .word_bank import parse_wb_draft, refine_wb_draft, show_wb_draft

def refine_wb_draft_tui():
    while True:
        print("Paste a WordBank:")
        try:
            lines=get_lines_until_empty()
            wbd=parse_wb_draft(lines)
            with open_session() as s:
                refine_wb_draft(s, wbd)
            show_wb_draft(wbd)
        except Exception as e:
            print(str(e))
