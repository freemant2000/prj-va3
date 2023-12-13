from vocabassistant3.va3 import *

def add_or_use_word_def(s):
  word=input()
  wds=get_word_def(s, word)
  if wds:
    print("Found existing")
    for wd in wds:
      show_word_def(wd)
  else:
    print("Not found")

def show_word_def(wd):
    print(wd.id, wd.word)
    for m in wd.meanings:
      print("\t"+m.meaning)

def use_word_def():
    wd=WordDef(id=0, word="hand")
    wd.add_meaning("n", "手")
    wd.add_meaning("v", "遞給")
    print(wd.id, wd.word, wd.get_display())
    for m in wd.meanings:
        print(m.p_of_s)
        print(m.meaning)

def add_word_def(s: Session):
    wd=WordDef(word="hand")
    wd.add_meaning("n", "手")
    wd.add_meaning("v", "遞給")
    s.add(wd)
    s.commit()
    print(wd.id)

with open_session() as s:
  add_or_use_word_def(s)
