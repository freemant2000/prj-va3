from dataclasses import dataclass
from operator import and_
from sqlalchemy import ForeignKey, Sequence as Seq, select, or_
from sqlalchemy.orm import Session, joinedload, Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer
from typing import Sequence, List
from .db_base import Base

class WordDef(Base):
    __tablename__="word_defs"
    id: Mapped[int]=mapped_column(Integer, Seq("word_def_seq"), primary_key=True)
    word: Mapped[str]=mapped_column(String)
    meanings: Mapped[List["WordMeaning"]]=relationship("WordMeaning", order_by="asc(WordMeaning.idx)", back_populates="wd", cascade="all, delete-orphan")
    def add_meaning(self, p_of_s: str, meaning: str, forms:Sequence[str]=[])->None:
        m=WordMeaning()
        m.p_of_s=p_of_s
        m.meaning=meaning
        m.idx=len(self.meanings)
        m.set_forms(forms)
        self.meanings.append(m)
    def get_full_word(self, forms_indice: Sequence[int])->str:
        word=self.word
        if not forms_indice:
            return word
        first_idx=forms_indice[0]
        first_forms=self.meanings[first_idx].get_forms()
        if all(self.meanings[m_idx].get_forms()==first_forms for m_idx in forms_indice):
            fw=self.meanings[first_idx].add_forms(word)
            return fw
        else:
            forms=[f"{m_idx}:"+",".join(self.meanings[m_idx].get_forms()) for m_idx in forms_indice]
            forms.insert(0, word)
            fw="; ".join(forms)
            return fw
    def get_display(self)->str:
        return self.word+"\t"+self.get_meanings()
    def get_meanings(self)->str:
        return u"、".join([f"{m.meaning}({m.p_of_s})" for m in self.meanings])
    def get_selected_meanings(self, m_indice:Sequence[int])->str:
        return u"、".join([f"{self.meanings[m_i].meaning}({self.meanings[m_i].p_of_s})" for m_i in m_indice])
    def get_all_m_indice(self)->str:
        return ",".join([str(idx) for idx in range(len(self.meanings))])
    def __str__(self) -> str:
        return f"WordDef {self.word} with {len(self.meanings)} meanings"
    def is_usage(self, wd: "WordDef", m_indice: str)->bool:
        if wd.id != self.id or wd.word != self.word:
            return False
        for idx, m_idx in enumerate(m_indice.split(",")):
            if m_idx.endswith("F"):
                m_idx=m_idx.rstrip("F")
            m_idx=int(m_idx)
            if m_idx<len(self.meanings):
                wm1=self.meanings[m_idx]
                wm2=wd.meanings[idx]
                if wm1.p_of_s!=wm2.p_of_s or wm1.meaning!=wm2.meaning:
                    return False
            else:
                return False
        return True

@dataclass
class WordUsage:
    wd: WordDef
    m_indice: str

class WordMeaning(Base):
    __tablename__="word_meanings"
    wd_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_defs.id"), primary_key=True)
    wd: Mapped[WordDef]=relationship("WordDef", back_populates="meanings")
    idx: Mapped[int]=mapped_column(Integer, primary_key=True)
    p_of_s: Mapped[str]=mapped_column(String)
    meaning: Mapped[str]=mapped_column(String)
    form1: Mapped[str]=mapped_column(String)
    form2: Mapped[str]=mapped_column(String)
    form3: Mapped[str]=mapped_column(String)
    
    def has_forms(self)->bool:
        return self.form1!=None
    def set_forms(self, forms: Sequence[str]):
        if forms:
            self.form1=forms.pop(0)
            if forms:
                self.form2=forms.pop(0)
                if forms:
                    self.form3=forms.pop(0)
    def add_forms(self, word):
        def concat(*ss):
            return ", ".join([s for s in ss if s])
        if word==self.form1 and word==self.form2:
            fw=f"{word} x3"
            fw=concat(fw, self.form3)
        elif word==self.form1:
            fw=f"{word} x2"
            fw=concat(fw, self.form2, self.form3)
        else:
            fw=concat(word, self.form1, self.form2, self.form3)
        return fw
    def get_forms(self)->List[str]:
        forms=[self.form1, self.form2, self.form3]
        forms=[f for f in forms if f]
        return forms
    def get_display(self)->str:
        return f"{self.p_of_s},{self.meaning}"

def get_word_meaning(s: Session, wd_id: int, idx: int)->WordMeaning:
    q=select(WordMeaning).where(WordMeaning.wd_id==wd_id, WordMeaning.idx==idx)\
        .options(joinedload(WordMeaning.wd))
    r=s.scalars(q)
    wm=r.first()
    return wm

def get_word_meanings(s: Session, wd_ids: Sequence[int], indice: Sequence[int])->Sequence[WordMeaning]:
    q=select(WordMeaning)\
        .options(joinedload(WordMeaning.wd)) \
        .order_by(WordMeaning.wd_id.asc(), WordMeaning.idx.asc())
    q=q.where(or_(*[
        and_(WordMeaning.wd_id==wd_ids[i], WordMeaning.idx==indice[i]) for i in range(len(wd_ids))]))
    r=s.scalars(q)
    wms=r.unique().all()
    return wms

def get_word_defs(s: Session, wd_ids: Sequence[int])->Sequence[WordDef]:
  q=select(WordDef).where(WordDef.id.in_(wd_ids)).options(joinedload(WordDef.meanings)) \
      .order_by(WordDef.id.asc())
  r=s.scalars(q)
  wds=r.unique().all()
  return wds

def get_word_def_by_id(s: Session, wd_id: int)->WordDef:
  q=select(WordDef).where(WordDef.id==(wd_id))
  r=s.scalars(q)
  wd=r.unique().first()
  return wd

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

