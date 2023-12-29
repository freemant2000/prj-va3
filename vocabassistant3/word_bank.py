from dataclasses import dataclass, field
import re
from typing import Dict, Sequence, List, Tuple
from sqlalchemy import or_, select, ForeignKey, Sequence as Seq
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship, joinedload
from sqlalchemy.types import String, Integer
from .db_base import Base
from .word_def import WordMeaningsParser, get_word_def, WordDef, get_word_def_by_id, WordUsage, parse_full_word

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
        m_indice=self.m_indice.split(",")
        m_indice=[int(m_idx.rstrip("F")) for m_idx in m_indice if m_idx.endswith("F")]
        fw=self.wd.get_full_word(m_indice)
        return fw
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
        if self.get_strict_cands():
            raise ValueError("There are words identical to existing ones")
        if self.mismatches:
            wd=next(iter(self.mismatches.keys()))
            raise ValueError(f"Trying to use a word but the word or meanings are different: {wd.word}")
        for wd in self.wds:
            if wd in self.word_usages:
                pass
            elif wd in self.word_updates:
                if not wd.meanings:
                    raise ValueError(f"Trying to update {wd.word} but no meaning is given")
            else:
                if not wd.meanings:
                    raise ValueError(f"No ID is specified for {wd.word} but no meaning is given")

    def get_strict_cands(self)->Dict[WordDef, List[WordDef]]:
        s_cands={}
        for wd, cands in self.cands.items():
            rcs=[c for c in cands if wd.word==c.word]
            if rcs:
                s_cands[wd]=rcs
        return s_cands

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
    else: # new WordDef, implicit usage or undecided
        wds=get_word_def(s, wd.word)
        if wds:
            if len(wds)==1:  # usually should be only one match
                wd2=wds[0]
                m_indice=wd2.infer_m_indice(wd)
                if m_indice:
                    wbd.word_usages[wd]=WordUsage(wd2, m_indice)
                else:
                    wbd.mismatches[wd]=wd2
            else:
                wbd.cands[wd]=wds
        else:
            pass #new or error

def add_wb_draft(s: Session, wbd: WordBankDraft)->WordBank:
    refine_wb_draft(s, wbd)
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
    
def parse_wb_draft(lines: List[str])->WordBankDraft:    
    wbd=WordBankDraft()
    wbd.wds=[]
    head=lines.pop(0)
    m=re.match(r"\[(.+)\]", head)
    if not m:
      raise ValueError("The name for the WordBank should be like [abc], not "+head)
    wbd.name=m.group(1)
    for line in lines:
      if line.startswith(" ") or line.startswith("\t"): # a meaning
            wmp.parse_line(line)
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
                if "=" in word_str or ">" in word_str or "<" in word_str: 
                    raise ValueError(f"{word_str} contains invalid characters")
            word, forms=parse_full_word(word_str)
            wd=WordDef(id=None, word=word)
            wbd.wds.append(wd)
            wmp=WordMeaningsParser(wd, forms)
            if usage_str:
                try:
                    wd_id, m_indice=usage_str.split(",")
                except:
                    raise ValueError(f"Comma expected in {usage_str}")
                m_indice=m_indice.replace("-", ",")
                wbd.word_usages[wd]=WordUsage(WordDef(id=int(wd_id)), m_indice)
                wd.id=wd_id
            elif update_str:
                wd_id=int(update_str)
                wbd.word_updates[wd]=wd_id
                wd.id=wd_id
    return wbd

