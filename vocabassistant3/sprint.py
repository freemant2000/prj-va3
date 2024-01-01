from dataclasses import dataclass, field
from itertools import groupby
from sqlalchemy import ForeignKey, Table, Column, select, Sequence as Seq
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import String, Integer, Date
from typing import Dict, List, Sequence
import datetime   
from .db_base import Base
from .word_def import WordDef, WordUsage, get_word_def, get_word_meaning
from .sentence import Sentence, SentenceDraft, get_snt, get_snts_from_keywords, parse_snt_draft, refine_snt_draft
from .practice import Practice, Student, get_practice
from .word_bank import WordBank, BankWord

class ExeciseWord(Base):
    __tablename__="exercise_word"
    e_id: Mapped[int]=mapped_column(Integer, ForeignKey("exercises.id"), primary_key=True)
    exec: Mapped["Exercise"]=relationship("Exercise", back_populates="ews")
    wd_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_defs.id"), primary_key=True)
    wd: Mapped[WordDef]=relationship(WordDef)
    m_indice: Mapped[str]=mapped_column(String)
    def __str__(self) -> str:
        return f"exercise word {self.wd.word}"

exec_snt_tbl=Table("exercise_snt", Base.metadata, 
                    Column("e_id", Integer, ForeignKey("exercises.id"), primary_key=True),
                    Column("s_id", Integer, ForeignKey("sentences.id"), primary_key=True))

class Exercise(Base):
    __tablename__="exercises"
    id: Mapped[int]=mapped_column(Integer, Seq("exercise_seq"), primary_key=True)
    dt: Mapped[datetime.date]=mapped_column(Date)
    ews: Mapped[List[ExeciseWord]]=relationship(ExeciseWord, order_by="asc(ExeciseWord.wd_id)", back_populates="exec", cascade="all, delete-orphan")
    snts: Mapped[List[Sentence]]=relationship("Sentence", secondary=exec_snt_tbl)
    def __str__(self) -> str:
        return f"exercise {self.id} {len(self.ews)} words"
    def uses_snt(self, snt: Sentence)->bool:
        return any(s for s in self.snts if s.id==snt.id)

sprint_prac_tbl=Table("sprint_practice", Base.metadata, 
                    Column("sp_id", Integer, ForeignKey("sprints.id"), primary_key=True),
                    Column("p_id", Integer, ForeignKey("practices.id"), primary_key=True))

sprint_exec_tbl=Table("sprint_exercise", Base.metadata, 
                    Column("sp_id", Integer, ForeignKey("sprints.id"), primary_key=True),
                    Column("e_id", Integer, ForeignKey("exercises.id"), primary_key=True))

class Sprint(Base):
    __tablename__="sprints"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    start_dt: Mapped[datetime.date]=mapped_column(Date)
    pracs: Mapped[List[Practice]]=relationship("Practice", secondary=sprint_prac_tbl, order_by=sprint_prac_tbl.c.p_id)
    execs: Mapped[List[Exercise]]=relationship("Exercise", secondary=sprint_exec_tbl, order_by=sprint_exec_tbl.c.e_id)
    stu_id: Mapped[int]=mapped_column(Integer, ForeignKey("students.id"))
    stu: Mapped[Student]=relationship(Student)
    
    def is_hard(self, bw: BankWord)->bool:
        return any(prac.is_hard(bw) for prac in self.pracs)
    def find_bank_words(self, word: str)->Sequence[BankWord]:
        bws=[]
        for prac in self.pracs:
            bws.extend(prac.find_bank_words(word))
        return bws
    def get_bws(self)->Sequence[BankWord]:
        bws=[]
        for p in self.pracs:
            bws2=p.get_bws()
            for bw in bws2:
                if bw not in bws:
                    bws.append(bw)
        return bws
    def get_all_bws(self)->Sequence[BankWord]:
        bws=[]
        for p in self.pracs:
            bws2=p.get_all_bws()
            for bw in bws2:
                if bw not in bws:
                    bws.append(bw)
        return bws
    def clear_hard(self):
        for p in self.pracs:
            p.clear_hard()
    def mark_all_hard(self, hard: bool):
        for p in self.pracs:
            p.mark_all_hard(hard)
    def mark_words_hard(self, w_indice: Sequence[int], hard: bool=True):
        bws=self.get_bws()
        selected_bws=[]
        for idx in w_indice:
            if not 0<=idx<len(bws):
                raise ValueError(f"Invalid index {idx}")
            selected_bws.append(bws[idx])
        for p in self.pracs:
            p.mark_words_hard(selected_bws, hard)
    def set_assessed_dt(self):
        for p in self.pracs:
            p.set_assessed_dt()
    def del_exec(self, idx: int)->Exercise:
        if 0<=idx<len(self.execs):
            exec=self.execs.pop(idx)
            return exec
        else:
            raise ValueError(f"Index must be 0-{len(self.execs)-1}")
    def contains_prac(self, prac: Practice)->bool:
        return any(p for p in self.pracs if p.id==prac.id)
    def add_prac(self, prac: Practice):
        if self.contains_prac(prac):
            raise ValueError("The practice is already in the sprint")
        else:
            self.pracs.append(prac)
    def uses_snt(self, snt: Sentence)->bool:
        return any(exec for exec in self.execs if exec.uses_snt(snt))

def add_sprint(s: Session, stu_id: int, p_ids: Sequence[int])->Sprint:
    sp=Sprint()
    sp.stu_id=stu_id
    sp.start_dt=datetime.date.today()
    for p_id in p_ids:
        prac=get_practice(s, p_id)
        sp.pracs.append(prac)
    s.add(sp)
    return sp

def get_exec(s: Session, e_id: int)->Exercise:
  q=select(Exercise).where(Exercise.id==e_id) \
    .options(joinedload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Exercise.snts).joinedload(Sentence.keywords))
  r=s.scalars(q)
  exec=r.unique().first()
  return exec

def get_sprint(s: Session, sp_id: int)->Sprint:
  q=select(Sprint).where(Sprint.id==sp_id) \
    .options(joinedload(Sprint.pracs).joinedload(Practice.hard_w_indice)) \
    .options(joinedload(Sprint.pracs).joinedload(Practice.wb).selectinload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Sprint.execs).selectinload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings))
  r=s.scalars(q)
  sp=r.unique().first()
  return sp

def get_sprints_for(s: Session, stu_id: int)->List[Sprint]:
  q=select(Sprint).where(Sprint.stu_id==stu_id) \
    .options(joinedload(Sprint.pracs).joinedload(Practice.wb).selectinload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Sprint.execs).selectinload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings))
  r=s.scalars(q)
  sps=r.unique().all()
  return sps

def get_sprint_for_exec(s: Session, e_id: int)->Sprint:
    q=select(Sprint).join(Sprint.execs).where(Exercise.id==e_id) \
        .options(joinedload(Sprint.pracs).joinedload(Practice.hard_w_indice)) \
        .options(joinedload(Sprint.pracs).joinedload(Practice.wb).selectinload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
        .options(joinedload(Sprint.execs).selectinload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings))
    r=s.scalars(q)
    sp=r.unique().first()
    return sp

def get_revision_dates(s: Session, sp_id: int)->Dict[ExeciseWord, List[datetime.date]]:
    q=select(Exercise, ExeciseWord).join(sprint_exec_tbl).join(Sprint) \
        .where(Sprint.id==sp_id, ExeciseWord.e_id==Exercise.id) \
        .order_by(ExeciseWord.wd_id, ExeciseWord.m_indice, Exercise.dt)
    r=s.execute(q)
    rs=r.unique().all()
    rds={}
    for k, sub_seq in groupby(rs, key=lambda r: (r[1].wd_id, r[1].m_indice)):
        ds=[]
        for exec, ew in sub_seq:
            ds.append(exec.dt)
        rds[ew]=ds
    return rds

@dataclass
class ExerciseDraft:
    words: List[str] = field(default_factory=list)
    wus: Dict[str, WordUsage] = field(default_factory=dict)
    sds: List[SentenceDraft] = field(default_factory=list)
    snt_cands: List[Sentence] = field(default_factory=list)
    extra_kws: List[str] = field(default_factory=list)
    used_sds: List[SentenceDraft] = field(default_factory=list)

    def check_complete(self):
        for word in self.words:
            if word not in self.wus:
                raise ValueError(f"{word} is undefined")
        for sd in self.sds:
            sd.check_complete()

def select_words_make_draft(sp: Sprint, indice: Sequence[int]):
    pass


def add_exec_draft(s: Session, sp: Sprint, ed: ExerciseDraft)->Exercise:
    refine_exec_draft(s, sp, ed)
    ed.check_complete()
    exec=Exercise()
    exec.dt=datetime.date.today()
    for kw in ed.words:
        wu=ed.wus[kw]
        ew=ExeciseWord(wd_id=wu.wd.id, m_indice=wu.m_indice)
        exec.ews.append(ew)
    for sd in ed.sds:
        if sd.snt_id==None: # new sentence
            snt=Sentence(text=sd.text)
            for kw in sd.keywords:
                wm=sd.kw_meanings[kw]
                wm=get_word_meaning(s, wm.wd_id, wm.idx)
                snt.keywords.append(wm)
                s.add(snt)
        else:
            snt=get_snt(s, sd.snt_id)
        exec.snts.append(snt)
    s.add(exec)
    sp.execs.append(exec)
    return exec

def load_exec_draft(path: str)->ExerciseDraft:
  with open(path) as f:
    lines=f.readlines()
    ed=parse_exec_draft(lines)
    return ed

def parse_exec_draft(lines: Sequence[str])->ExerciseDraft:
    ed=ExerciseDraft()
    expect_words=True
    snt_lines=[]
    for line in lines:
        if line:
            if expect_words:
                line=line.strip()
                if line.count("=")==len(line): # ==== line
                    expect_words=False
                    continue
                ps=line.split("<=")
                if len(ps)==1:
                    ed.words.append(ps[0])
                elif len(ps)==2:
                    word=ps[0]
                    wu_parts=ps[1].split(",")
                    if len(wu_parts)!=2:
                        raise ValueError(f"Invalid word usage {wu_parts} for {word}")
                    wd_id=int(wu_parts[0])
                    m_indice=wu_parts[1].replace("-", ",")
                    ed.words.append(word)
                    ed.wus[word]=WordUsage(WordDef(id=wd_id), m_indice=m_indice)
                else:
                    raise ValueError(f"Invalid word line {line}")
            else:
                if line.startswith(" ") or line.startswith("\t"):
                    snt_lines.append(line)
                else: # start a new sentence draft
                    line=line.strip()
                    if snt_lines:
                        ed.sds.append(parse_snt_draft(snt_lines))
                    snt_lines=[line]
    if snt_lines:
        ed.sds.append(parse_snt_draft(snt_lines))
    return ed

def refine_exec_draft(s: Session, sp: Sprint, ed: ExerciseDraft):
    for word in ed.words:
        if not (word in ed.wus):
            bws=sp.find_bank_words(word)
            if bws:
                wu=WordUsage(wd=bws[0].wd, m_indice=bws[0].m_indice)
                ed.wus[word]=wu
            else:
                wds=get_word_def(s, word)
                if len(wds)==1:
                    wd=wds[0]
                    wu=WordUsage(wd=wd, m_indice=wd.get_all_m_indice())
                    ed.wus[word]=wu
    for sd in ed.sds:
        refine_snt_draft(s, sd)
    ed.snt_cands=[t[0] for t in get_snts_from_keywords(s, ed.words)]
    ed.extra_kws.clear()
    ed.used_sds.clear()
    for sd in ed.sds:
        if sd.snt_id!=None:
            snt=get_snt(s, sd.snt_id)
            for wm in snt.keywords:
                if wm.wd.word not in ed.words:
                    ed.extra_kws.append(wm.wd.word)
            if sp.uses_snt(snt):
                ed.used_sds.append(sd)
        else:
            for kw in sd.keywords:
                if kw not in ed.words:
                    ed.extra_kws.append(kw)

