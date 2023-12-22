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
    
    def get_meanings(self)->str:
        m_indice=self.m_indice.split(",")
        m_indice=[int(m_idx.rstrip("F")) for m_idx in m_indice]
        return self.wd.get_selected_meanings(m_indice)
    def get_full_word(self)->str:
        word=self.wd.word
        m_indice=self.m_indice.split(",")
        m_idx=next((m_idx for m_idx in m_indice if m_idx.endswith("F")), None)
        if m_idx:
           m_idx=int(m_idx.rstrip("F"))
           fw=self.wd.meanings[m_idx].add_forms(word)
           return fw
        else:
           return word
    def is_same(self, bw: "BankWord")->bool:
        return self.wd_id==bw.wd_id and self.m_indice==bw.m_indice
       
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
    word_updates: Dict[WordDef, int]= field(default_factory=dict)
    cands: Dict[WordDef, List[WordDef]]= field(default_factory=dict)
    mismatches: Dict[WordDef, List[WordDef]]= field(default_factory=dict)
    upd_targets: Dict[WordDef, WordDef]= field(default_factory=dict)

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
            raise ValueError("Trying to use a word but the word or meanings are different")
        for wd in self.wds:
            if wd in self.word_usages:
                pass
            elif wd in self.word_updates:
                if not wd.meanings:
                    raise ValueError(f"Trying to update {wd.word} but no meaning is given")
            else:
                if not wd.meanings:
                    raise ValueError(f"No ID is specified for {wd.word} but no meaning is given")

def refine_wb_draft(s: Session, wbd: WordBankDraft):
  wbd.cands.clear()
  wbd.mismatches.clear()
  wbd.upd_targets.clear()
  for wd in wbd.wds:
    if wd in wbd.word_usages: # use existing WordDef
        wu=wbd.word_usages[wd]
        wd.id=wu.wd.id
        wd2=get_word_def_by_id(s, wu.wd.id)
        if not wd2.is_usage(wd, wu.m_indice):
            wbd.mismatches[wd]=wd2
    elif wd in wbd.word_updates: # update existing WordDef
        wd2=get_word_def_by_id(s, wbd.word_updates[wd])
        wbd.upd_targets[wd]=wd2
    else: # new WordDef or undecided
        wds=get_word_def(s, wd.word)
        if wds:
            wbd.cands[wd]=wds

def add_wb_draft(s: Session, wbd: WordBankDraft)->WordBank:
    wbd.check_complete()
    for wd in wbd.wds:
        if wd in wbd.word_usages:
            pass
        elif wd in wbd.word_updates:
            s.merge(wd)
        else:
            s.add(wd)
    s.flush()  #make sure the IDs are assigned
    wb=WordBank(name=wbd.name)
    for (idx, wd) in enumerate(wbd.wds):
        if wd in wbd.word_usages:
            wu=wbd.word_usages[wd]
            bw=BankWord(idx=idx, wd_id=wu.wd.id, m_indice=wu.m_indice)
        else: # new or update
            bw=BankWord(idx=idx, wd_id=wd.id, m_indice=wd.get_all_m_indice())
        wb.bws.append(bw)
    s.add(wb)
    return wb

def load_wb_draft(path: str)->WordBankDraft:
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
                ps=line.split(":")
                if len(ps)==2:
                    if forms:
                        raise ValueError(f"Forms provided along with the word, but are specified again in {line}")
                    forms=[f.strip() for f in ps[1].split(",")]
                elif len(ps)==1:
                    pass #apply the forms following the word (if any)
                else:
                    raise ValueError(f"Too many colons in {line}")
                try:
                    p_of_s, m=ps[0].split(",")
                    wbd.wds[-1].add_meaning(p_of_s, m, forms)
                    forms=[]  
                except:
                    raise ValueError(f"comma missing in {ps[0]}")
      else: #start a new word
        line=line.strip()
        if line:
            usage_str=None
            update_str=None
            if "<=" in line:  # use some meanings from a WordDef
                word_str, usage_str=line.split("<=")
            elif "=>" in line:  # update a WordDef
                word_str, update_str=line.split("=>")
            else:
                word_str=line
            word, forms=parse_full_word(word_str)
            wd=WordDef(id=None, word=word)
            wbd.wds.append(wd)
            if usage_str:
                wd_id, m_indice=update_str.split(",")
                m_indice=m_indice.replace("-", ",")
                wbd.word_usages[wd]=WordUsage(WordDef(id=int(wd_id)), m_indice)
                wd.id=wd_id
            elif update_str:
                wd_id=int(update_str)
                wbd.word_updates[wd]=wd_id
                wd.id=wd_id
    return wbd

def parse_full_word(fw: str)->(str, List[str]):
    ps=fw.split(",")
    ps=[p.strip() for p in ps]
    word=ps.pop(0)
    return (word, ps)
