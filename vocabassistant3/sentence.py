from ast import keyword
from dataclasses import dataclass, field
from sqlalchemy import select, ForeignKey, Table, Column, ForeignKeyConstraint, Sequence as Seq
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import String, Integer
from typing import Dict, List, Sequence

from vocabassistant3.word_bank import show_word_def
from .db_base import Base
from .word_def import WordDef, WordMeaning, get_word_def, get_word_meanings

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
    text: str
    keywords: Sequence[str] = field(default_factory=list)
    kw_meanings: Dict[str, WordMeaning] = field(default_factory=dict)
    kw_cands: Dict[str, Sequence[WordMeaning]] = field(default_factory=dict)    

    def check_complete(self):
        for kw in self.keywords:
            if not kw in self.kw_meanings:
                raise ValueError(f"Keyword {kw} in {self.text} has no assigned meaning")

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
    print("WordMeaning candidates")
    for kw, cands in sd.kw_cands.items():
        print(f"For {kw}")
        for wm in cands:
            print(f"\t{kw}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")

def show_snt(snt: Sentence):
    print(f"Sentence {snt.text}")
    for wm in snt.keywords:
        print(f"\t{wm.wd.word}<={wm.wd_id},{wm.idx},{wm.p_of_s},{wm.meaning}")

def refine_snt_draft(s: Session, sd: SentenceDraft):
    sd.kw_cands.clear()
    for kw in sd.keywords:
        if not (kw in sd.kw_meanings):
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


