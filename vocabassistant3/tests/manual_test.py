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

wam=WordAndMeaning("wind")
wam.add_meaning("n", "風")
wam.add_meaning("v", "緾繞")
add_word_and_meaning(wam)