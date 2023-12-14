from vocabassistant3.va3 import *

def show_sprint(sp):
    print(sp.id, sp.start_dt)
    for p in sp.pracs:
      print(p.id, p.wb.name)
      for wd in p.wb.wds:
        print("\t"+wd.get_display())
    for e in sp.execs:
      print(e.id, e.dt)
      for wd in e.wds:
        print("\t"+wd.get_display())

def show_exec(exec):
    print(exec.id, exec.dt)
    for wd in exec.wds:
      print(wd.word)
    for snt in exec.snts:
      print(snt.text)

def show_word_def(wd):
    print(wd.word)
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

def show_exec(exec: Exercise):
  print(exec)
  print(len(exec.snts))
  for ew in exec.ews:
    print(ew)

def show_word_bank(wb: WordBank):
  print(wb)

with open_session() as s:
  wb=get_word_bank(s, 0)
  show_word_bank(wb)
  
