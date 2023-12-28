from .cmd_handler import CmdHandler
from .console_utils import get_lines_until_empty
from ..db_base import open_session
from ..sentence import Sentence, SentenceDraft, add_snt_draft, get_snts_from_keywords, parse_snt_draft, refine_snt_draft

def snts_tui():
    cmds={"find": ("Search for sentences with keywords", find_snts_tui),
          "rs": ("Refine a sentence draft", refine_snt_draft_tui),
          "as": ("Add an exercise", add_snt_draft_tui)}
    ch=CmdHandler("snts>", cmds)
    ch.main_loop()

def find_snts_tui():
    kws=[kw.strip() for kw in input("Input keyword(s) like dog,house: ").split(",")]
    with open_session() as s:
        snts=get_snts_from_keywords(s, kws)
    for snt, mc in snts:
        show_snt(snt)

def input_snt_draft()->SentenceDraft:
    print("Paste a new sentence, followed by indented keywords:")
    lines=get_lines_until_empty()
    sd=parse_snt_draft(lines)
    return sd

def add_snt_draft_tui():
    sd=input_snt_draft()
    with open_session() as s:
        add_snt_draft(s, sd)
        s.commit()
        print("OK")

def refine_snt_draft_tui():
    sd=input_snt_draft()
    with open_session() as s:
        refine_snt_draft(s, sd)
    show_snt_draft(sd)

def show_snt_draft(sd: SentenceDraft, used=False):
    if used:
        status="Used in sprint"
    else:
        status="Complete" if sd.is_complete() else "Incomplete"
    print(f"{sd.text} ({status})")
    if sd.snt_candidates:
        print("Sentence candidates")
        for snt in sd.snt_candidates:
            print(f"{snt.text}<={snt.id}")
    for kw in sd.keywords:
        if kw in sd.kw_meanings:
            wm=sd.kw_meanings[kw]
            print(f"\t{kw}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")
        else:
            print("\t"+kw)
    if sd.kw_cands:
        print("WordMeaning candidates")
        for kw, cands in sd.kw_cands.items():
            print(f"For {kw}")
            for wm in cands:
                print(f"\t{kw}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")

def show_snt(snt: Sentence):
    print(f"{snt.text}")
    for wm in snt.keywords:
        print(f"\t{wm.wd.word}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")
