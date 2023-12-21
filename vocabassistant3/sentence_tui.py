from .cmd_handler import CmdHandler
from .db_base import open_session
from .console_utils import get_lines_until_empty
from .sentence import Sentence, SentenceDraft, get_snts_from_keywords, parse_snt_draft, refine_snt_draft

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

def add_snt_draft_tui():
    pass

def refine_snt_draft_tui():
    while True:
        print("Paste a new sentence, followed by indented keywords:")
        try:
            lines=get_lines_until_empty()
            sd=parse_snt_draft(lines)
            with open_session() as s:
                refine_snt_draft(s, sd)
            show_snt_draft(sd)
        except Exception as e:
            print(str(e))

def show_snt_draft(sd: SentenceDraft):
    print(sd.text)
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
    print("Complete" if sd.is_complete() else "Incomplete")

def show_snt(snt: Sentence):
    print(f"{snt.text}")
    for wm in snt.keywords:
        print(f"\t{wm.wd.word}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")
