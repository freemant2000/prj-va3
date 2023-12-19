from typing import Sequence
from .db_base import open_session
from .console_utils import get_lines_until_empty
from .word_bank import WordBank, get_word_bank, get_word_banks, parse_wb_draft, refine_wb_draft, show_wb_draft

def show_word_banks_tui():
    offset=int(input("Input starting index: "))
    with open_session() as s:
        wbs=get_word_banks(s, offset, 30)
        for wb in wbs:
            show_word_bank_summary(wb)

def show_word_bank_summary(wb: WordBank):
    print(f"{wb.id} {wb.name} {wb.get_no_words()}")

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
