from dataclasses import dataclass, field
from operator import or_
import re
from typing import Dict, Sequence, List
from sqlalchemy import select, ForeignKey, Sequence as Seq
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship, joinedload
from sqlalchemy.types import String, Integer
from .db_base import Base
from .word_def import get_word_def, WordDef, get_word_def_by_id, WordUsage

class BankWord(Base):
    __tablename__="bank_word"
    wb_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_banks.id"), primary_key=True)
    wb: Mapped["WordBank"]=relationship("WordBank", back_populates="bws")
    idx: Mapped[int]=mapped_column(Integer, primary_key=True)
    wd_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_defs.id"))
    wd: Mapped[WordDef]=relationship(WordDef)
    m_indice: Mapped[str]=mapped_column(String)

class WordBank(Base):
    __tablename__="word_banks"
    id: Mapped[int]=mapped_column(Integer, Seq("word_bank_seq"), primary_key=True)
    name: Mapped[str]=mapped_column(String)
    bws: Mapped[List[BankWord]]=relationship(BankWord, order_by="asc(BankWord.idx)", back_populates="wb", cascade="all")
    def __str__(self) -> str:
        return f"WordBank {self.id} {self.name} {len(self.bws)} words"
    def get_no_words(self)->int:
        return len(self.bws)

def get_word_bank(s: Session, wb_id: int)->WordBank:
  q=select(WordBank).where(WordBank.id==wb_id) \
    .options(joinedload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings))
  r=s.scalars(q)
  wb=r.unique().first()
  return wb

def get_word_banks(s: Session, offset: int, limit: int)->List[WordBank]:
  q=select(WordBank) \
    .options(joinedload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
    .order_by(WordBank.id).offset(offset).limit(limit)
  r=s.scalars(q)
  wbs=r.unique().all()
  return wbs

def find_word_banks(s: Session, kw: str, limit: int=20)->List[WordBank]:
  q=select(WordBank) \
    .join(WordBank.bws).join(BankWord.wd) \
    .where(or_(WordBank.name.contains(kw), WordDef.word==kw)) \
    .options(joinedload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
    .order_by(WordBank.id).limit(limit)
  r=s.scalars(q)
  wbs=r.unique().all()
  return wbs

@dataclass
class WordBankDraft:
    name: str=""
    wds: Sequence[WordDef] = field(default_factory=list)
    word_usages: Dict[WordDef, WordUsage]= field(default_factory=dict)
    cands: Dict[WordDef, List[WordDef]]= field(default_factory=dict)
    mismatches: Dict[WordDef, List[WordDef]]= field(default_factory=dict)

    def is_complete(self)->bool:
        try:
            self.check_complete()
            return True
        except:
            return False

    def check_complete(self):
        if self.cands:
            raise ValueError("There are words identical to existing ones")
        if self.mismatches:
            raise ValueError("WordDef ID is specified but the word or meanings are different")
        for wd in self.wds:
            if not wd.meanings:
                raise ValueError(f"No ID is specified for {wd.word} but no meaning is given")

def refine_wb_draft(s: Session, wbd: WordBankDraft):
  wbd.cands.clear()
  wbd.mismatches.clear()
  for wd in wbd.wds:
    if wd in wbd.word_usages:
        wu=wbd.word_usages[wd]
        wd.id=wu.wd.id
        wd2=get_word_def_by_id(s, wu.wd.id)
        if not wd2.is_usage(wd, wu.m_indice):
            wbd.mismatches[wd]=wd2
    else:
        wds=get_word_def(s, wd.word)
        if wds:
            wbd.cands[wd]=wds

def add_wb_draft(s: Session, wbd: WordBankDraft)->WordBank:
    wbd.check_complete()
    for wd in wbd.wds:
        if not (wd in wbd.word_usages):
            s.add(wd)
    s.flush()  #make sure the IDs are assigned
    wb=WordBank(name=wbd.name)
    for (idx, wd) in enumerate(wbd.wds):
        if not (wd in wbd.word_usages):
            bw=BankWord(idx=idx, wd_id=wd.id, m_indice=wd.get_all_m_indice())
        else:
            wu=wbd.word_usages[wd]
            bw=BankWord(idx=idx, wd_id=wu.wd.id, m_indice=wu.m_indice)
        wb.bws.append(bw)
    s.add(wb)
    return wb

def load_wb_input(path: str)->WordBankDraft:
  with open(path) as f:
    lines=f.readlines()
    wbd=parse_wb_draft(lines)
    return wbd
    
def parse_wb_draft(lines: Sequence[str])->WordBankDraft:    
    wbd=WordBankDraft()
    wbd.wds=[]
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
            wbd.word_usages[wd]=WordUsage(WordDef(id=int(wd_id)), m_indice)
    return wbd

