from vocabassistant3.word_def import WordDef
from .cmd_handler import CmdHandler
from .db_base import open_session
from .console_utils import get_lines_until_empty
from .word_bank import BankWord, WordBank, WordBankDraft, get_word_bank, get_word_banks, parse_wb_draft, refine_wb_draft

offset=0

def word_banks_tui():
    global offset
    cmds={"list": ("List Word Banks", list_word_banks),
      "reset": ("Restart from the beginning", reset),
      "show": ("Show the words in a Word Bank", show_word_bank_tui),
      "refine": ("Refine a Word Bank Draft", refine_wb_draft_tui)}
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

def show_word_bank_tui():
    wb_id=int(input("Input WordBank ID: "))
    with open_session() as s:
        wb=get_word_bank(s, wb_id)
        show_word_bank(wb)

def show_word_bank(wb: WordBank):
    print(f"{wb.id} {wb.name} {wb.get_no_words()}")
    for bw in wb.bws:
        show_bank_word(bw)

def show_bank_word(bw: BankWord):
    print(f"{bw.wd.word.ljust(20)} {bw.wd.get_meanings()}")

def refine_wb_draft_tui():
    print("Paste a Word Bank Draft and then press Enter:")
    lines=get_lines_until_empty()
    wbd=parse_wb_draft(lines)
    with open_session() as s:
        refine_wb_draft(s, wbd)
        show_wb_draft(wbd)

def show_wb_draft(wbd: WordBankDraft):
    print(f"WordBank {wbd.name} ({'complete' if wbd.is_complete() else 'incomplete'})")
    for wd in wbd.wds:
        if wd in wbd.word_usages:
            wu=wbd.word_usages[wd]
            print(f"{wd.word}<={wu.wd.id},{wu.m_indice.replace(',', '-')}")
        else:
            print(wd.word)
        for wm in wd.meanings:
            print("\t"+wm.get_display())
    if wbd.cands:
        print(f"Possible matches")
        for wd, wds in wbd.cands.items():
            for old_wd in wds:
                show_word_def(old_wd)
    if wbd.mismatches:
        print(f"Mismatches")
        for wd, wd2 in wbd.mismatches.items():
            print(wd.word)
            print("-------")
            show_word_def(wd2)

def show_word_def(wd: WordDef):
    print(f"{wd.word}<={wd.id},{wd.get_all_m_indice().replace(',', '-')}")
    for m in wd.meanings:
      print("\t"+m.get_display())

