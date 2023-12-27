from .cmd_handler import CmdHandler
from .console_utils import get_lines_until_empty
from ..word_def import UpdateType, WordDef, WordDefDraft, WordMeaning, get_similar_words, parse_wd_draft, refine_wd_draft, save_wd_draft
from ..db_base import open_session

def word_defs_tui():
    cmds={
      "find": ("Find a word def", search_word_def),
      "refine": ("Refine a word def draft", refine_wd_draft_tui),
      "add": ("Add a word def from a draft", lambda: save_wd_draft_tui(UpdateType.NEW)),
      "extend": ("Save a word def draft to extend a word def", lambda: save_wd_draft_tui(UpdateType.EXTENDS)),
      "update": ("Save a word def draft to update a meaning in a word def", lambda: save_wd_draft_tui(UpdateType.SET_MEANING)),
      "force-save": ("Save a word def draft to drastically update a word def", lambda: save_wd_draft_tui(UpdateType.DRASTIC))}
    ch=CmdHandler("wds>", cmds)
    ch.main_loop()

def search_word_def():
    prefix=input("Input the first part of a word: ")
    with open_session() as s:
        wds=get_similar_words(s, prefix)
        for wd in wds:
            show_word_def(wd)

def show_word_def(wd: WordDef):
    print(f"{wd.get_full_word().ljust(20)} {wd.get_meanings()}")

def refine_wd_draft_tui():
    wdd=input_wd_draft()
    with open_session() as s:
        refine_wd_draft(s, wdd)
        show_wd_draft(wdd)

def input_wd_draft()->WordDefDraft:
    print("Paste a word def draft and then press Enter:")
    lines=get_lines_until_empty()
    wdd=parse_wd_draft(lines)
    return wdd
def save_wd_draft_tui(upd_type: UpdateType):
    wbd=input_wd_draft()
    with open_session() as s:
        s.begin()
        save_wd_draft(s, wbd, upd_type)
        s.commit()
        print("OK")

def show_wd_draft(wdd: WordDefDraft):
    if wdd.is_extends:
        status="extends"
    elif wdd.is_diff_meaning_text:
        status="set meaning"
    elif wdd.is_same:
        status="no change"
    else:
        status="drastic change"
    print(f"{wdd.wd.word}")
    for wm in wdd.wd.meanings:
        show_meaning(wm)
    if wdd.target:
        print(f"Update target ({status})")
        show_word_def(wdd.target)
    elif wdd.cands:
        print(f"Possible matches")
        for wd in wdd.cands:
            show_word_def(wd)

def show_word_def(wd: WordDef):
    print(f"{wd.word}@{wd.id}")
    for m in wd.meanings:
        show_meaning(m)

def show_meaning(m: WordMeaning):
    forms=m.get_forms()
    if forms:
        fs=":"+", ".join(forms)
    else:
        fs=""
    print("\t"+m.get_display()+fs)
