from dataclasses import dataclass, field
import re
from vocabassistant3.va3 import *
from typing import Dict

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
    print(f"Id {wd.id} {wd.word}")
    for m in wd.meanings:
      print(f"\t{m.idx} {m.meaning}")

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
  name: str=""
  wds: Sequence[WordDef] = field(default_factory=list)
  use_old_wds: Dict[WordDef, WordBankItemOld]= field(default_factory=dict)

def check_wb_draft(s: Session, wbd: WordBankDraft):
  for wd in wbd.wds:
    if not (wd in wbd.use_old_wds):
      wds=get_word_def(s, wd.word)
      if wds:
        print(f"Possible matches for {wd.word}")
        for wd2 in wds:
          show_word_def(wd2)

def show_wb_draft(wbd: WordBankDraft):
  print("WordBank "+wbd.name)
  for e in wbd.wds:
    print(e)
  print("Using existing WordDefs")
  for (wd, io) in wbd.use_old_wds.items():
    print(wd)
    print(io.wb_id, io.m_indice)

def load_wb_input()->WordBankDraft:
  wbd=WordBankDraft()
  wbd.wds=[]
  with open("vocabassistant3/tests/test_wb_input.txt") as f:
    lines=f.readlines()
    head=lines.pop(0)
    m=re.match(r"\[(.+)\]", head)
    if not m:
      raise ValueError("The name for the WordBank should be like [abc], not "+head)
    wbd.name=m.group(1)
    for line in lines:
      if line.startswith(" ") or line.startswith("\t"): # a meaning
          line=line.strip()
          if line:
            p_of_s, m=line.split(",")
            wbd.wds[-1].add_meaning(p_of_s, m)
      else: #start a new word
        line=line.strip()
        if line:
          tp=line.split("<=")
          wd=WordDef(id=None, word=tp[0])
          wbd.wds.append(wd)
          if len(tp)==2: #use a WordDef
            _, p2=tp
            wd_id, m_indice=p2.split(",")
            m_indice=m_indice.replace("-", ",")
            wbd.use_old_wds[wd]=WordBankItemOld(int(wd_id), m_indice)
  return wbd

with open_session() as s:
  wbd=load_wb_input()
  show_wb_draft(wbd)
  #check_wb_draft(s, wbd)