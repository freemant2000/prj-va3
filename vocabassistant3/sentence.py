from ast import keyword
from dataclasses import dataclass, field
from sqlalchemy import select, ForeignKey, Table, Column, ForeignKeyConstraint, Sequence as Seq
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import String, Integer
from typing import Dict, List, Sequence

from vocabassistant3.word_bank import show_word_def
from .db_base import Base
from .word_def import WordDef, WordMeaning, get_word_def, get_word_meaning, get_word_meanings

snt_wd_tbl=Table("snt_keywords", Base.metadata, 
                    Column("snt_id", Integer, ForeignKey("sentences.id"), primary_key=True),
                    Column("wd_id", Integer, primary_key=True),
                    Column("wm_idx", Integer, primary_key=True),
                    ForeignKeyConstraint(["wd_id", "wm_idx"], ["word_meanings.wd_id", "word_meanings.idx"]))

class Sentence(Base):
    __tablename__="sentences"
    id: Mapped[int]=mapped_column(Integer, Seq("sentence_seq"), primary_key=True)
    text: Mapped[str]=mapped_column(String)
    keywords: Mapped[List[WordMeaning]]=relationship("WordMeaning", secondary=snt_wd_tbl)

def get_snt(s: Session, id: int)->Sentence:
  q=select(Sentence).where(Sentence.id==id) \
      .options(joinedload(Sentence.keywords).joinedload(WordMeaning.wd))
  r=s.scalars(q)
  return r.unique().first()

def get_snts(s: Session, words: Sequence[str])->Sequence[Sentence]:
  q=select(Sentence).where(Sentence.keywords.any(WordMeaning.wd.has(WordDef.word.in_(words)))) \
      .options(joinedload(Sentence.keywords).joinedload(WordMeaning.wd)) \
      .order_by(Sentence.id.asc())
  r=s.scalars(q)
  return r.unique().all()

def get_snts_from_text(s: Session, text: str)->Sequence[Sentence]:
  q=select(Sentence).where(Sentence.text==text) \
      .options(joinedload(Sentence.keywords).joinedload(WordMeaning.wd)) \
      .order_by(Sentence.id.asc())
  r=s.scalars(q)
  return r.unique().all()

@dataclass
class SentenceDraft:
    text: str = ""
    keywords: List[str] = field(default_factory=list)
    kw_meanings: Dict[str, WordMeaning] = field(default_factory=dict)
    kw_cands: Dict[str, Sequence[WordMeaning]] = field(default_factory=dict)    

    def check_complete(self):
        for kw in self.keywords:
            if not kw in self.kw_meanings:
                raise ValueError(f"Keyword {kw} in {self.text} has no assigned meaning")

    def is_complete(self):
        return self.keywords and len(self.keywords)==len(self.kw_meanings)

def add_snt_draft(s: Session, sd: SentenceDraft):
    sd.check_complete()
    snt=Sentence(text=sd.text)
    snt.keywords=get_word_meanings(s, \
                        [wm.wd_id for wm in sd.kw_meanings.values()], \
                        [wm.idx for wm in sd.kw_meanings.values()])
    s.add(snt)

def show_snt_draft(sd: SentenceDraft):
    print(sd.text)
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
    print(f"Sentence {snt.text}")
    for wm in snt.keywords:
        print(f"\t{wm.wd.word}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")

def refine_snt_draft(s: Session, sd: SentenceDraft):
    sd.kw_cands.clear()
    #TODO if snt_id is specified, check if it is correct and matches the text.
    #if snt_id is not specified, use the text to search for candidates.
    #get_snts_from_text(sd.text)

    for kw in sd.keywords:
        if kw in sd.kw_meanings:
            wm=sd.kw_meanings[kw]
            wm2=get_word_meaning(s, wm.wd_id, wm.idx)
            if wm2:
                sd.kw_meanings[kw]=wm2
            else:
                raise ValueError(f"Cannot find Meaning for {kw} at {wm.wd_id} {wm.idx}")
        else:
            wds=get_word_def(s, kw)
            if wds:
                if len(wds)==1:
                    wd=wds[0]
                    if len(wd.meanings)==1:
                        sd.kw_meanings[kw]=wd.meanings[0]
                    else:
                        sd.kw_cands[kw]=wd.meanings
                else:
                    sd.kw_cands[kw]=[wm for wm in wd.meanings for wd in wds]


def load_snt_draft(path: str)->SentenceDraft:
  with open(path) as f:
    lines=f.readlines()
    return parse_snt_draft(lines)

def parse_snt_draft(lines: Sequence[str])->SentenceDraft:
    sd=SentenceDraft()
    head=lines.pop(0).strip()
    if not head:
      raise ValueError("The first line is empty")
    sd.text=head
    for line in lines:
      if line.startswith(" ") or line.startswith("\t"): # a keyword
            line=line.strip()
            if line:
                ps=line.split("<=")
                if len(ps)==1:
                    sd.keywords.append(line)
                elif len(ps)==2:
                    kw=ps[0]
                    wm_str=ps[1]
                    wm_parts=wm_str.split(",")
                    n=len(wm_parts)
                    if n!=2 and n!=4:
                        raise ValueError(f"Invalid WordMeaning {wm_str}")
                    sd.keywords.append(kw)
                    sd.kw_meanings[kw]=WordMeaning(wd_id=int(wm_parts[0]), idx=int(wm_parts[1]))
      else:
          raise ValueError("Indented keyword expected")
    return sd
