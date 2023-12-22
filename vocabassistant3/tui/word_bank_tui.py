from .word_bank_search_tui import search_word_banks
from .cmd_handler import CmdHandler
from .console_utils import get_lines_until_empty
from ..word_def import WordDef, WordMeaning
from ..db_base import open_session
from ..word_bank import BankWord, WordBank, WordBankDraft, add_wb_draft, get_word_bank, get_word_banks, parse_wb_draft, refine_wb_draft

offset=0

def word_banks_tui():
    global offset
    cmds={"list": ("List word banks", list_word_banks),
      "reset": ("Restart the listing from the beginning", reset),
      "search": ("Perform a keyword search for word banks", search_word_banks),
      "show": ("Show the words in a word bank", show_word_bank_tui),
      "refine": ("Refine a word bank draft", refine_wb_draft_tui),
      "save": ("Save a word bank draft as a word bank", save_wb_draft_tui)}
    offset=0
    ch=CmdHandler("wbs>", cmds)
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
    print(f"{bw.get_full_word().ljust(20)} {bw.get_meanings()}")

def refine_wb_draft_tui():
    wbd=input_wb_draft()
    with open_session() as s:
        refine_wb_draft(s, wbd)
        show_wb_draft(wbd)

def input_wb_draft()->WordBankDraft:
    print("Paste a Word Bank Draft and then press Enter:")
    lines=get_lines_until_empty()
    wbd=parse_wb_draft(lines)
    return wbd

def save_wb_draft_tui():
    wbd=input_wb_draft()
    with open_session() as s:
        s.begin()
        add_wb_draft(s, wbd)
        s.commit()
        print("OK")

def show_wb_draft(wbd: WordBankDraft):
    print(f"WordBank {wbd.name} ({'complete' if wbd.is_complete() else 'incomplete'})")
    for wd in wbd.wds:
        if wd in wbd.word_usages:
            wu=wbd.word_usages[wd]
            print(f"{wd.word}<={wu.wd.id},{wu.m_indice.replace(',', '-')}")
        elif wd in wbd.word_updates:
            print(f"{wd.word}=>{wbd.word_updates[wd]}")
        else:
            print(wd.word)
        for wm in wd.meanings:
            show_meaning(wm)
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
    if wbd.upd_targets:
        print(f"Update targets")
        for wd, wd2 in wbd.upd_targets.items():
            print("-------")
            show_word_def(wd)
            show_word_def(wd2)

def show_word_def(wd: WordDef):
    print(f"{wd.word}<={wd.id},{wd.get_all_m_indice().replace(',', '-')}")
    for m in wd.meanings:
        show_meaning(m)

def show_meaning(m: WordMeaning):
    forms=m.get_forms()
    if forms:
        fs=":"+", ".join(forms)
    else:
        fs=""
    print("\t"+m.get_display()+fs)

