from sqlalchemy import ForeignKey, Table, Column, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer, Date, Boolean
from typing import List, Sequence
import datetime   

class Base(DeclarativeBase):
    pass

class WordDef(Base):
    __tablename__="word_defs"
    id: Mapped[int]=mapped_column(primary_key=True)
    word: Mapped[str]=mapped_column(String)
    meanings: Mapped[List["WordMeaning"]]=relationship("WordMeaning", order_by="asc(WordMeaning.idx)", back_populates="wd")
    def add_meaning(self, p_of_s: str, meaning: str)->None:
        m=WordMeaning()
        m.p_of_s=p_of_s
        m.meaning=meaning
        self.meanings.append(m)
    def get_display(self)->str:
        return self.word+"\t"+self.get_meanings()
    def get_meanings(self)->str:
        return u"、".join([f"{m.meaning}({m.p_of_s})" for m in self.meanings])

class WordMeaning(Base):
    __tablename__="word_meanings"
    wd_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_defs.id"), primary_key=True)
    wd: Mapped[WordDef]=relationship("WordDef", back_populates="meanings")
    idx: Mapped[int]=mapped_column(Integer, primary_key=True)
    p_of_s: Mapped[str]=mapped_column(String)
    meaning: Mapped[str]=mapped_column(String)

bank_wd_tbl=Table("bank_word", Base.metadata, 
                    Column("wb_id", Integer, ForeignKey("word_banks.id"), primary_key=True),
                    Column("idx", Integer, primary_key=True),
                    Column("wd_id", Integer, ForeignKey("word_defs.id")))


class WordBank(Base):
    __tablename__="word_banks"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String)
    wds: Mapped[List[WordDef]]=relationship("WordDef", secondary=bank_wd_tbl)

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

exec_wd_tbl=Table("exercise_word_def", Base.metadata, 
                    Column("e_id", Integer, ForeignKey("exercises.id"), primary_key=True),
                    Column("wd_id", Integer, ForeignKey("word_defs.id"), primary_key=True))

exec_snt_tbl=Table("exercise_snt", Base.metadata, 
                    Column("e_id", Integer, ForeignKey("exercises.id"), primary_key=True),
                    Column("s_id", Integer, ForeignKey("sentences.id"), primary_key=True))

class Exercise(Base):
    __tablename__="exercises"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    dt: Mapped[datetime.date]=mapped_column(Date)
    wds: Mapped[List[WordDef]]=relationship("WordDef", secondary=exec_wd_tbl)
    snts: Mapped[List[Sentence]]=relationship("Sentence", secondary=exec_snt_tbl)

sprint_prac_tbl=Table("sprint_practice", Base.metadata, 
                    Column("sp_id", Integer, ForeignKey("sprints.id"), primary_key=True),
                    Column("p_id", Integer, ForeignKey("practices.id"), primary_key=True))

class Practice(Base):
    __tablename__="practices"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    wb_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_banks.id"))
    wb: Mapped[WordBank]=relationship("WordBank")
    fr_idx: Mapped[int]=mapped_column(Integer)
    to_idx: Mapped[int]=mapped_column(Integer)
    hard_only: Mapped[bool]=mapped_column(Boolean)
    assess_dt: Mapped[datetime.date]=mapped_column(Date)

    def get_wds(self)->Sequence[WordDef]:
        return self.wb.wds[self.fr_idx:self.to_idx+1]

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

