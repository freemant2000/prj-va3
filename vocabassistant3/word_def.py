from dataclasses import dataclass, field
from enum import Enum
from operator import and_
from sqlalchemy import ForeignKey, Sequence as Seq, select, or_
from sqlalchemy.orm import Session, joinedload, Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer
from typing import Sequence, List, Tuple
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
        gs={}
        for idx in forms_indice:
            forms=",".join(self.meanings[idx].get_forms())
            if forms in gs.keys():
                gs[forms].append(idx)
            else:
                gs[forms]=[idx]
        if len(gs)==1:
            forms,indice=next(iter(gs.items()))
            first_idx=indice[0]
            fw=self.meanings[first_idx].add_forms(word)
            return fw
        else:
            all_forms=[]
            for forms,indice in gs.items():
                indice_str="-".join([str(idx) for idx in indice])
                all_forms+=[f"{indice_str}:"+forms]
            all_forms.insert(0, word)
            fw="; ".join(all_forms)
            return fw
    def get_display(self)->str:
        return self.word+"\t"+self.get_meanings()
    def get_meanings(self)->str:
        return u"、".join([f"{m.meaning}({m.p_of_s})" for m in self.meanings])
    def get_selected_meanings(self, m_indice:Sequence[int])->str:
        try:
            return u"、".join([f"{self.meanings[m_i].meaning}({self.meanings[m_i].p_of_s})" for m_i in m_indice])
        except IndexError:
            raise ValueError(f"Index out of range for word {self.word} with ID {self.id}")
    def get_all_m_indice(self)->str:
        return ",".join([str(idx)+("F" if self.meanings[idx].has_forms() else "") for idx in range(len(self.meanings))])
    def __str__(self) -> str:
        return f"WordDef {self.word} with {len(self.meanings)} meanings"
    def get_meanings_subset(self, m_indice: str)->List["WordMeaning"]:
        wms=[]
        for m_idx in m_indice.split(","):
            if m_idx.endswith("F"):
                m_idx=m_idx.rstrip("F")
                incl_forms=True
            else:
                incl_forms=False
            m_idx=int(m_idx)
            if m_idx<len(self.meanings):
                wm=self.meanings[m_idx].clone()
                if not incl_forms:
                    wm.clear_forms()
                wms.append(wm)
        return wms

    def is_usage(self, wd: "WordDef", m_indice: str)->bool:
        if wd.id != self.id or wd.word != self.word:
            return False
        for idx, m_idx in enumerate(m_indice.split(",")):
            if m_idx.endswith("F"):
                m_idx=m_idx.rstrip("F")
            m_idx=int(m_idx)
            if m_idx<len(self.meanings):
                wm1=self.meanings[m_idx]
                if idx>=len(wd.meanings):
                    return False
                wm2=wd.meanings[idx]
                if wm1.p_of_s!=wm2.p_of_s or wm1.meaning!=wm2.meaning:
                    return False
            else:
                return False
        return True
    def infer_m_indice(self, wd: "WordDef")->str:
        if wd.word != self.word:
            return None
        m_indice=[]
        for wm in wd.meanings:
            m_idx=next((idx for idx, wm2 in enumerate(self.meanings) if wm2.is_same_cnt(wm)), -1)
            if m_idx>=0:
                m_indice.append(str(m_idx)+("F" if wm.has_forms() else ""))
            else:
                return None
        m_indice=sorted(m_indice)
        return ",".join(m_indice)
    def is_extends(self, wd: "WordDef")->bool:
        if wd.word != self.word:
            return False
        if len(self.meanings)<=len(wd.meanings):
            return False;
        for m_idx, wm in enumerate(wd.meanings):
            if not wm.is_same_cnt(self.meanings[m_idx]):
                return False
        return True
    def is_diff_meaning_text(self, wd: "WordDef")->bool:
        if wd.word != self.word:
            return False
        if len(self.meanings)!=len(wd.meanings):
            return False;
        for wm, wm2 in zip(self.meanings, wd.meanings):
            if not wm.is_diff_meaning_text(wm2):
                return False
        return True
    def is_same(self, wd: "WordDef")->bool:
        if wd.word != self.word:
            return False
        if len(self.meanings)!=len(wd.meanings):
            return False;
        for wm, wm2 in zip(self.meanings, wd.meanings):
            if not wm.is_same_cnt(wm2):
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
        elif self.form1 and self.form1==self.form2:
            fw=f"{word}, {self.form1} x2"
            fw=concat(fw, self.form3)
        else:
            fw=concat(word, self.form1, self.form2, self.form3)
        return fw
    def get_forms(self)->List[str]:
        forms=[self.form1, self.form2, self.form3]
        forms=[f for f in forms if f]
        return forms
    def get_display(self)->str:
        return f"{self.p_of_s},{self.meaning}"
    def is_same_cnt(self, wm: "WordMeaning")->bool:
        return self.p_of_s==wm.p_of_s and self.meaning==wm.meaning and self.get_forms()==wm.get_forms() 
    def is_diff_meaning_text(self, wm: "WordMeaning")->bool:
        return self.p_of_s==wm.p_of_s and self.meaning!=wm.meaning and self.get_forms()==wm.get_forms() 
    def clear_forms(self):
        self.form1=self.form2=self.form3=None
    def clone(self)->"WordMeaning":
        wm=WordMeaning()
        wm.p_of_s=self.p_of_s
        wm.meaning=self.meaning
        wm.idx=self.idx
        wm.set_forms(self.get_forms())
        return wm

@dataclass
class WordDefDraft:
    wd: WordDef=None
    target: WordDef=None
    cands: List[WordDef]=field(default_factory=list)
    is_same: bool=False
    is_extends: bool=False
    is_diff_meaning_text: bool=False

class UpdateType(Enum):
    EXTENDS="E"
    SET_MEANING="M"
    DRASTIC="D"
    NEW="N"

def refine_wd_draft(s: Session, wdd: WordDefDraft):
    wds=get_word_def(s, wdd.wd.word)
    wdd.cands=[]
    wdd.target=None
    wdd.is_same=False
    wdd.is_extends=False
    wdd.is_diff_meaning_text=False
    if len(wds):
        if len(wds)==1:
            wdd.target=wds[0]
            wdd.is_same=wdd.wd.is_same(wdd.target)
            wdd.is_extends=wdd.wd.is_extends(wdd.target)
            wdd.is_diff_meaning_text=wdd.wd.is_diff_meaning_text(wdd.target)
        else:
            wdd.cands=wds
    else:
        wdd.target=None

def parse_full_word(fw: str)->Tuple[str, List[str]]:
    ps=fw.split(",")
    ps=[p.strip() for p in ps]
    word=ps.pop(0)
    return (word, ps)

def load_wd_draft(path: str)->WordDefDraft:
  with open(path) as f:
    lines=f.readlines()
    wdd=parse_wd_draft(lines)
    return wdd

def parse_wd_draft(lines: List[str])->WordDefDraft:    
    wdd=WordDefDraft()
    word_str=lines.pop(0).strip()
    word, forms=parse_full_word(word_str)
    wd=WordDef(id=None, word=word)
    wdd.wd=wd
    wmp=WordMeaningsParser(wd, forms)
    for line in lines:
        wmp.parse_line(line)
    return wdd

def save_wd_draft(s: Session, wdd: WordDefDraft, upd_type: UpdateType):
    refine_wd_draft(s, wdd)
    if upd_type==UpdateType.NEW:
        if wdd.target:
            raise ValueError("Target identified but trying to add as new")
    else:
        if not wdd.target:
            raise ValueError("No target identified in the word def draft")
    if not wdd.wd.meanings:
        raise ValueError("No meaning specified")
    if upd_type==UpdateType.NEW:
        s.add(wdd.wd)
    else:
        if upd_type==UpdateType.EXTENDS:
            if wdd.is_extends:
                raise ValueError("The word def draft is not extending an old word def")
        elif upd_type==UpdateType.SET_MEANING:
            if wdd.is_diff_meaning_text:
                raise ValueError("The word def draft is not updating a meaning in an old word def")
        elif upd_type==UpdateType.DRASTIC:
            pass
        else:
            raise ValueError(f"Unknown update type: {upd_type}")
        wdd.wd.id=wdd.target.id
        s.merge(wdd.wd)

class WordMeaningsParser:
    def __init__(self, wd: WordDef, forms: List[str]) -> None:
        self.wd=wd
        self.forms=forms
    def parse_line(self, line: str):
        if line.startswith(" ") or line.startswith("\t"): # a meaning
            line=line.strip()
            if line:
                ps=line.split(":")
                if len(ps)==2:
                    if self.forms:
                        raise ValueError(f"Forms provided along with the word, but are specified again in {line}")
                    self.forms=[f.strip() for f in ps[1].split(",")]
                elif len(ps)==1:
                    pass #apply the forms following the word (if any)
                else:
                    raise ValueError(f"Too many colons in {line}")
                try:
                    p_of_s, m=ps[0].split(",")
                    self.wd.add_meaning(p_of_s, m, self.forms)
                    self.forms=[]  
                except:
                    raise ValueError(f"comma missing in {ps[0]}")
        else:
            raise ValueError(f"Indentation expected in {line}")

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

def get_similar_words(s: Session, pref: str, limit:int=5)->List[WordDef]:
  return get_words_by_pattern(s, pref+"%", limit)

def get_word_def(s: Session, word: str, limit:int=5)->List[WordDef]:
  return get_words_by_pattern(s, word, limit)

def get_words_by_pattern(s: Session, pattern: str, limit:int=5)->List[WordDef]:
  q=select(WordDef).where(WordDef.word.like(pattern)).options(joinedload(WordDef.meanings)) \
      .order_by(WordDef.id.asc()).limit(limit)
  r=s.scalars(q)
  wds=r.unique().all()
  return wds

