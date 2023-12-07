from gettext import find
from vocabassistant3.va3 import *


# wds=get_wd_in_exercise(0)
# for wd in wds:
#     print(wd)
# snts=get_snts_in_exercise(0)
# for s in snts:
#     print(s)

# wams=get_word_and_meanings([0, 1, 3])
# for e in wams:
#     print(e.get_display())

# wam=WordAndMeaning("wind")
# wam.add_meaning("n", "風")
# wam.add_meaning("v", "緾繞")
# add_word_and_meaning(wam)

def show_execs_in_sprint():
    sp_id=0
    sp=get_sprint(sp_id)
    print(f"Sprint {sp.id} started on {sp.start_dt}")
    for wam in sp.wams:
        print(wam.get_display())

def show_words_in_sprint():
    sp_id=0
    wd_ids=get_wd_in_sprint(sp_id)
    wams=get_word_and_meanings(wd_ids)
    for wam in wams:
        print(wam.get_display())

def show_exercise():
    sp_id=0
    wd_ids=get_wd_in_sprint(sp_id)
    wams=get_word_and_meanings(wd_ids)
    for wam in wams:
        print(wam.get_display())

def find_applicable_snts():
    words=["steep", "valley"]
    snts=find_sentences(words)
    load_keywords(snts)
    for snt in snts:
        print(snt.text)
        for k in snt.keywords:
            print("\t"+k.get_display())

show_execs_in_sprint()