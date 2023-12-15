from sqlalchemy import Sequence as Seq, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import Integer, String
from vocabassistant3.word_bank import WordBank
from .practice import Practice
from .db_base import Base

class Student(Base):
    __tablename__="students"
    id: Mapped[int]=mapped_column(Integer, Seq("student_seq"), primary_key=True)
    name: Mapped[str]=mapped_column(String)
    pracs: Mapped[Practice]=relationship(Practice, back_populates="student")

def get_student(s: Session, stu_id: int)->Student:
    q=select(Student).where(Student.id==stu_id)\
        .options(joinedload(Student.pracs).joinedload(Practice.wb).joinedload(WordBank.bws))
    stu=s.scalars(q).first()
    return stu