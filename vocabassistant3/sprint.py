from dataclasses import dataclass, field
from sqlalchemy import ForeignKey, Table, Column, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import String, Integer, Date
from typing import Dict, List, Sequence, Tuple
import datetime   
from .db_base import Base
from .word_def import WordDef, WordMeaning, WordUsage
from .sentence import Sentence, SentenceDraft, get_snts_from_text, parse_snt_draft, refine_snt_draft, show_snt, show_snt_draft
from .practice import Practice
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
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    dt: Mapped[datetime.date]=mapped_column(Date)
    ews: Mapped[List[ExeciseWord]]=relationship(ExeciseWord, order_by="asc(ExeciseWord.wd_id)", back_populates="exec")
    snts: Mapped[List[Sentence]]=relationship("Sentence", secondary=exec_snt_tbl)
    def __str__(self) -> str:
        return f"exercise {self.id} {len(self.ews)} words"

sprint_prac_tbl=Table("sprint_practice", Base.metadata, 
                    Column("sp_id", Integer, ForeignKey("sprints.id"), primary_key=True),
                    Column("p_id", Integer, ForeignKey("practices.id"), primary_key=True))

sprint_exec_tbl=Table("sprint_exercise", Base.metadata, 
                    Column("sp_id", Integer, ForeignKey("sprints.id"), primary_key=True),
                    Column("idx", Integer, primary_key=True),
                    Column("e_id", Integer, ForeignKey("exercises.id")))

class Sprint(Base):
    __tablename__="sprints"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    start_dt: Mapped[datetime.date]=mapped_column(Date)
    pracs: Mapped[List[Practice]]=relationship("Practice", secondary=sprint_prac_tbl)
    execs: Mapped[List[Exercise]]=relationship("Exercise", secondary=sprint_exec_tbl, order_by=sprint_exec_tbl.c.idx)
    
    def find_bank_words(self, word: str)->Sequence[BankWord]:
        bws=[]
        for prac in self.pracs:
            bws.extend(prac.find_bank_words(word))
        return bws

def get_exec(s: Session, e_id: int)->Exercise:
  q=select(Exercise).where(Exercise.id==e_id) \
    .options(joinedload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Exercise.snts).joinedload(Sentence.keywords))
  r=s.scalars(q)
  exec=r.unique().first()
  return exec

def get_sprint(s: Session, sp_id: int)->Sprint:
  q=select(Sprint).where(Sprint.id==sp_id) \
    .options(joinedload(Sprint.pracs).joinedload(Practice.wb).joinedload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Sprint.execs).joinedload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings))
  r=s.scalars(q)
  sp=r.unique().first()
  return sp

@dataclass
class ExerciseDraft:
    words: List[str] = field(default_factory=list)
    wus: Dict[str, WordUsage] = field(default_factory=dict)
    sds: List[SentenceDraft] = field(default_factory=list)

def select_words_make_draft(sp: Sprint, indice: Sequence[int]):
    pass

def add_exec_draft(s: Session, sp: Sprint, ed: ExerciseDraft):
    pass

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

def show_exec_draft(ed: ExerciseDraft):
    for word in ed.words:
        if word in ed.wus:
            wu=ed.wus[word]
            print(f"{word}<={wu.wd.id},{wu.m_indice.replace(',', '-')}")
        else:
            print(word)
    for st in ed.snt_texts:
        if st in ed.old_snts:
            snt=ed.old_snts[st]
            print(f"{st}<={snt.id}")
        elif st in ed.new_snt_drafts:
            sd=ed.new_snt_drafts[st]
            show_snt_draft(sd)
            
def refine_exec_draft(s: Session, sp: Sprint, ed: ExerciseDraft):
    for word in ed.words:
        if not (word in ed.wus):
            bws=sp.find_bank_words(word)
            if bws:
                wu=WordUsage(wd=bws[0].wd, m_indice=bws[0].m_indice)
                ed.wus[word]=wu
    for st in ed.snt_texts:
        if st in ed.new_snt_drafts:
            sd=ed.new_snt_drafts[st]
            refine_snt_draft(s, sd)
        elif not st in ed.old_snts:
            snts=get_snts_from_text(s, st)
            if snts:
                if len(snts)==1:
                    ed.old_snts[st]=snts[0]
                else:
                    print("Found multiple sentence matches")
                    for snt in snts:
                        show_snt(snt)
            else:
                print(f"Sentence {st} not found")

def show_sprint(sp: Sprint):
    print(f"Spring {sp.id} started on {sp.start_dt}")
    print("Practices")
    for p in sp.pracs:
      print(p.id, p.wb.name)
      for bw in p.get_bws():
        print("\t"+bw.wd.word)
    print("Exercises")
    for exec in sp.execs:
      show_exec(exec)

def show_exec(exec: Exercise):
    print(f"Exercise {exec.id} created on {exec.dt}")
    for ew in exec.ews:
      print("\t"+ew.wd.word)
    for snt in exec.snts:
      print("\t"+snt.text)
