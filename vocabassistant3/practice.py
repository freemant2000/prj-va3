from sqlalchemy import ForeignKey, Sequence as Seq, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import Integer, Date, Boolean, String
from datetime import date
from .db_base import Base
from .word_bank import WordBank, BankWord, get_word_bank
from .word_def import WordDef
from typing import List, Sequence, Tuple

class PracticeHard(Base):
    __tablename__="practice_hard"
    p_id: Mapped[int]=mapped_column(Integer, ForeignKey("practices.id"), primary_key=True)
    prac: Mapped["Practice"]=relationship("Practice", back_populates="hard_w_indice")
    w_idx: Mapped[int]=mapped_column(Integer, primary_key=True)

class Practice(Base):
    __tablename__="practices"
    id: Mapped[int]=mapped_column(Integer, Seq("practice_seq"), primary_key=True)
    wb_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_banks.id"))
    wb: Mapped[WordBank]=relationship("WordBank")
    fr_idx: Mapped[int]=mapped_column(Integer)
    to_idx: Mapped[int]=mapped_column(Integer)
    hard_only: Mapped[bool]=mapped_column(Boolean)
    assess_dt: Mapped[date]=mapped_column(Date)
    stu_id: Mapped[int]=mapped_column(Integer, ForeignKey("students.id"))
    student: Mapped["Student"]=relationship("Student", back_populates="pracs")
    # the indice are relative to the WordBank
    hard_w_indice: Mapped[List[PracticeHard]]=relationship(PracticeHard, back_populates="prac", cascade="all, delete-orphan")

    def get_bws(self)->Sequence[BankWord]:
        bws=self.wb.bws[self.fr_idx:self.to_idx+1]
        if self.hard_only:
            return [self.wb.bws[ph.w_idx] for ph in self.hard_w_indice]
        else:
            return bws
    def get_all_bws(self)->Sequence[BankWord]:
        bws=self.wb.bws[self.fr_idx:self.to_idx+1]
        return bws
    def get_no_words(self)->int:
        return self.to_idx-self.fr_idx+1 if not self.hard_only else len(self.hard_w_indice)
    def get_word_counts(self)->Tuple[int, int]:
        return (len(self.hard_w_indice), len(self.get_all_bws()))
    def is_hard(self, bw: BankWord)->bool:
        bws=self.get_all_bws()
        return any(bws[ph.w_idx-self.fr_idx].is_same(bw) for ph in self.hard_w_indice)
    def clear_hard(self):
        self.hard_w_indice.clear()
    def mark_all_hard(self, hard: bool):
        if hard:
            self.hard_w_indice.clear()
            bws2=self.wb.bws[self.fr_idx:self.to_idx+1]
            for idx, bw in enumerate(bws2):
                ph=PracticeHard(p_id=self.id, w_idx=self.fr_idx+idx)
                self.hard_w_indice.append(ph)
        else:
            self.clear_hard()
    def mark_words_hard(self, bws: Sequence[BankWord], hard=True):
        bws2=self.wb.bws[self.fr_idx:self.to_idx+1]
        for idx, bw in enumerate(bws2):
            if bw in bws:
                ph=PracticeHard(p_id=self.id, w_idx=self.fr_idx+idx)
                if hard:
                    self.hard_w_indice.append(ph)
                else:
                    ph2=next((ph for ph in self.hard_w_indice if ph.w_idx==self.fr_idx+idx), None)
                    if ph2:
                        self.hard_w_indice.remove(ph2)
    def set_assessed_dt(self):
        self.assess_dt=date.today()
    def find_bank_words(self, word: str)->Sequence[BankWord]:
        return [bw for bw in self.get_bws() if bw.wd.word==word]
    def get_display(self)->str:
        return f"{str(self)}\t{self.get_no_words()}\t{self.assess_dt}"
    def __str__(self) -> str:
        return f"{self.wb.name} {self.fr_idx}-{self.to_idx}"

class Student(Base):
    __tablename__="students"
    id: Mapped[int]=mapped_column(Integer, Seq("student_seq"), primary_key=True)
    name: Mapped[str]=mapped_column(String)
    pracs: Mapped[List[Practice]]=relationship(Practice, back_populates="student")

def get_student(s: Session, stu_id: int)->Student:
    q=select(Student).where(Student.id==stu_id)\
        .options(joinedload(Student.pracs).joinedload(Practice.wb).joinedload(WordBank.bws)) \
        .options(joinedload(Student.pracs).joinedload(Practice.hard_w_indice))
    stu=s.scalars(q).first()
    return stu

def get_all_bws(s: Session, stu_id: int)->Sequence[BankWord]:
    q=select(BankWord).select_from(Student).join(Student.pracs).join(Practice.wb).join(WordBank.bws).join(BankWord.wd).where(Student.id==stu_id).order_by(WordBank.id, BankWord.idx)\
        .options(joinedload(BankWord.wd).joinedload(WordDef.meanings))
    bws=s.scalars(q).unique().all()
    return bws

def get_practice(s: Session, p_id: int)->Practice:
    q=select(Practice).where(Practice.id==p_id)\
        .options(joinedload(Practice.wb))\
        .options(joinedload(Practice.hard_w_indice))
    r=s.scalars(q)
    p=r.unique().first()
    return p

def add_practice(s: Session, stu_id: int, wb_id: int, fr_idx: int, to_idx: int):
    wb=get_word_bank(s, wb_id)
    if not wb:
        raise ValueError(f"WordBank {wb_id} not found")
    fr_idx, to_idx=adjust_range(wb, fr_idx, to_idx)
    validate_range(fr_idx, to_idx)
    p=Practice(wb_id=wb_id, fr_idx=fr_idx, to_idx=to_idx, hard_only=False, assess_dt=date.today(), stu_id=stu_id)
    s.add(p)

def add_next_practice(s: Session, p_id: int):
    p=get_practice(p_id)
    if not p:
        raise ValueError(f"Practice {p_id} not found")
    fr_idx=p.to_idx+1
    to_idx=p.fr_idx+p.get_no_words()
    fr_idx, to_idx=adjust_range(p.wb, fr_idx, to_idx)
    validate_range(fr_idx, to_idx)
    p=Practice(wb_id=p.wb_id, fr_idx=fr_idx, to_idx=to_idx, hard_only=False, assess_dt=date.today())
    s.add(p)

def adjust_range(wb: WordBank, fr_idx: int, to_idx: int)->Tuple[int, int]:
    max_idx=len(wb.bws)-1
    fr_idx=min(fr_idx, max_idx)
    to_idx=min(to_idx, max_idx)
    return (fr_idx, to_idx)

def validate_range(fr_idx: int, to_idx: int):
    if fr_idx>to_idx or fr_idx<0:
        raise ValueError(f"Practice word range is invalid: {fr_idx} to {to_idx}")