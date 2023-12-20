from .cmd_handler import CmdHandler
from .db_base import open_session
from .console_utils import get_lines_until_empty
from .word_bank import WordBank, get_word_banks, parse_wb_draft, refine_wb_draft, show_wb_draft

offset=0

def word_banks_tui():
    global offset
    offset=0
    ch=CmdHandler("wb>", cmds)
    ch.main_loop()

def reset():
    global offset
    offset=0

def list_word_banks():
    global offset
    with open_session() as s:
        wbs=get_word_banks(s, offset, 30)
        offset += len(wbs)
        for wb in wbs:
            show_word_bank_summary(wb)

def show_word_bank_summary(wb: WordBank):
    print(f"{wb.id} {wb.name} {wb.get_no_words()}")

cmds={"list": ("List Word Banks", list_word_banks),
      "reset": ("Restart from the beginning", reset)}

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
