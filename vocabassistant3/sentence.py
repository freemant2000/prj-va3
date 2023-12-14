from sqlalchemy import select, ForeignKey, Table, Column, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import String, Integer
from typing import List, Sequence
from .db_base import Base
from .word_def import WordDef, WordMeaning

snt_wd_tbl=Table("snt_keywords", Base.metadata, 
                    Column("snt_id", Integer, ForeignKey("sentences.id"), primary_key=True),
                    Column("wd_id", Integer, primary_key=True),
                    Column("wm_idx", Integer, primary_key=True),
                    ForeignKeyConstraint(["wd_id", "wm_idx"], ["word_meanings.wd_id", "word_meanings.idx"]))

class Sentence(Base):
    __tablename__="sentences"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    text: Mapped[str]=mapped_column(String)
    keywords: Mapped[List[WordMeaning]]=relationship("WordMeaning", secondary=snt_wd_tbl)

def get_snts(s: Session, words: Sequence[str])->Sequence[Sentence]:
  q=select(Sentence).where(Sentence.keywords.any(WordMeaning.wd.has(WordDef.word.in_(words)))) \
      .options(joinedload(Sentence.keywords).joinedload(WordMeaning.wd)) \
      .order_by(Sentence.id.asc())
  r=s.scalars(q)
  return r.unique().all()
