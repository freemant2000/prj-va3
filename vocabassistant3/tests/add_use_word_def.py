from dataclasses import dataclass, field
from vocabassistant3.va3 import *
from typing import Union

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

@dataclass
class WordBankItemOld:
  wb_id: int
  m_indice: Sequence[int] = field(default_factory=list)

@dataclass
class WordBankDraft:
  items: Sequence[Union[WordDef, WordBankItemOld]] = field(default_factory=list)

def check_wb_draft():
  wbd=WordBankDraft()
  wbd.items=[WordDef()]

def show_wb_draft(wbd: WordBankDraft):
  for e in wbd.items:
    print(e)

def load_wb_input()->WordBankDraft:
  wbd=WordBankDraft()
  wbd.items=[]
  wb=None
  with open("vocabassistant3/tests/test_wb_input.txt") as f:
    for line in f.readlines():
      if line.startswith(" ") or line.startswith("\t"): # a meaning
          line=line.strip()
          if line:
            p_of_s, m=line.split(",")
            wb.add_meaning(p_of_s, m)
      else: #start a new word
        line=line.strip()
        if line:
          if wb:
            wbd.items.append(wb)
          wb=WordDef(word=line)
    if wb:
      wbd.items.append(wb)
  return wbd

# with open_session() as s:
#   add_or_use_word_def(s)

wbd=load_wb_input()
show_wb_draft(wbd)