from sqlalchemy import ForeignKey, Sequence as Seq, select
from sqlalchemy.orm import Session, joinedload, Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer
from typing import Sequence, List
from .db_base import Base

class WordDef(Base):
    __tablename__="word_defs"
    id: Mapped[int]=mapped_column(Integer, Seq("word_seq"), primary_key=True)
    word: Mapped[str]=mapped_column(String)
    meanings: Mapped[List["WordMeaning"]]=relationship("WordMeaning", order_by="asc(WordMeaning.idx)", back_populates="wd", cascade="all, delete-orphan")
    def add_meaning(self, p_of_s: str, meaning: str)->None:
        m=WordMeaning()
        m.p_of_s=p_of_s
        m.meaning=meaning
        m.idx=len(self.meanings)
        self.meanings.append(m)
    def get_display(self)->str:
        return self.word+"\t"+self.get_meanings()
    def get_meanings(self)->str:
        return u"、".join([f"{m.meaning}({m.p_of_s})" for m in self.meanings])
    def get_all_m_indice(self)->str:
        return ",".join([str(idx) for idx in range(len(self.meanings))])
    def __str__(self) -> str:
        return f"WordDef {self.word} with {len(self.meanings)} meanings"

class WordMeaning(Base):
    __tablename__="word_meanings"
    wd_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_defs.id"), primary_key=True)
    wd: Mapped[WordDef]=relationship("WordDef", back_populates="meanings")
    idx: Mapped[int]=mapped_column(Integer, primary_key=True)
    p_of_s: Mapped[str]=mapped_column(String)
    meaning: Mapped[str]=mapped_column(String)

def get_word_defs(s: Session, wd_ids: Sequence[int])->Sequence[WordDef]:
  q=select(WordDef).where(WordDef.id.in_(wd_ids)).options(joinedload(WordDef.meanings)) \
      .order_by(WordDef.id.asc())
  r=s.scalars(q)
  wds=r.unique().all()
  return wds

def del_word_def(s: Session, wd_id: int)->None:
  q=select(WordDef).where(WordDef.id==(wd_id))
  r=s.scalars(q)
  wd=r.unique().first()
  s.delete(wd)

def get_similar_words(s: Session, pref: str, limit:int=5)->Sequence[WordDef]:
  return get_words_by_pattern(s, pref+"%", limit)

def get_word_def(s: Session, word: str, limit:int=5)->Sequence[WordDef]:
  return get_words_by_pattern(s, word, limit)

def get_words_by_pattern(s: Session, pattern: str, limit:int=5)->Sequence[WordDef]:
  q=select(WordDef).where(WordDef.word.like(pattern)).options(joinedload(WordDef.meanings)) \
      .order_by(WordDef.id.asc())
  r=s.scalars(q)
  wds=r.unique().all()
  return wds

