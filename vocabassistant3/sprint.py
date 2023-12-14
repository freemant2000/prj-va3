from sqlalchemy import ForeignKey, Table, Column, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import String, Integer, Date
from typing import List
import datetime   
from .db_base import Base
from .word_def import WordDef
from .sentence import Sentence
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
