from sqlalchemy import ForeignKey, Sequence as Seq, select, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import Integer, String

from .db_base import Base
from .practice import Student, Practice, WordBank

tch_stu_tbl=Table("teacher_student", Base.metadata, 
                    Column("tch_id", Integer, ForeignKey("teachers.id"), primary_key=True),
                    Column("stu_id", Integer, ForeignKey("students.id"), primary_key=True))

class Teacher(Base):
    __tablename__="teachers"
    id: Mapped[int]=mapped_column(Integer, Seq("teacher_seq"), primary_key=True)
    gmail: Mapped[str]=mapped_column(String)
    stus: Mapped[Student]=relationship(Student, secondary=tch_stu_tbl)
    def teaches(self, stu: Student)->bool:
        return any(s for s in self.stus if s.id==stu.id)
    def check_teaches(self, stu: Student):
        if not self.teaches(stu):
            raise ValueError(f"You are not teaching that student")

def get_teacher(s: Session, tch_id: int)->Teacher:
    q=select(Teacher).where(Teacher.id==tch_id) \
        .options(joinedload(Teacher.stus) \
                 .joinedload(Student.pracs) \
                 .joinedload(Practice.wb) \
                 .selectinload(WordBank.bws))
    tch=s.scalars(q).unique().first()
    return tch

def get_teacher_by_email(s: Session, email: str)->Teacher:
    q=select(Teacher).where(Teacher.gmail==email) \
        .options(joinedload(Teacher.stus) \
                 .joinedload(Student.pracs) \
                 .joinedload(Practice.wb) \
                 .selectinload(WordBank.bws))
    tch=s.scalars(q).unique().first()
    return tch
