from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer
from typing import List

class Base(DeclarativeBase):
    pass

class WordDef(Base):
    __tablename__="word_defs"
    id: Mapped[int]=mapped_column(primary_key=True)
    word: Mapped[str]=mapped_column(String()) #order_by="word_meanings.idx", 
    meanings: Mapped[List["WordMeaning"]]=relationship("WordMeaning", back_populates="wd")

class WordMeaning(Base):
    __tablename__="word_meanings"
    wd_id: Mapped[int]=mapped_column(Integer(), ForeignKey("word_defs.id"), primary_key=True)
    idx: Mapped[int]=mapped_column(Integer(), primary_key=True)
    p_of_s: Mapped[str]=mapped_column(String())
    meaning: Mapped[str]=mapped_column(String())
    wd: Mapped[WordDef]=relationship("WordDef", back_populates="meanings")

