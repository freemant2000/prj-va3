from sqlalchemy import ForeignKey, Sequence as Seq, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from sqlalchemy.types import Integer, Date, Boolean
from datetime import date
from .db_base import Base
from .word_bank import WordBank, BankWord, get_word_bank
from typing import Sequence

class Practice(Base):
    __tablename__="practices"
    id: Mapped[int]=mapped_column(Integer, Seq("practice_seq"), primary_key=True)
    wb_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_banks.id"))
    wb: Mapped[WordBank]=relationship("WordBank")
    fr_idx: Mapped[int]=mapped_column(Integer)
    to_idx: Mapped[int]=mapped_column(Integer)
    hard_only: Mapped[bool]=mapped_column(Boolean)
    assess_dt: Mapped[date]=mapped_column(Date)

    def get_bws(self)->Sequence[BankWord]:
        return self.wb.bws[self.fr_idx:self.to_idx+1]

def get_practice(s: Session, p_id: int)->Practice:
    q=select(Practice).where(Practice.id==p_id).options(joinedload(Practice.wb))
    r=s.scalars(q)
    p=r.unique().first()
    return p

def add_practice(s: Session, wb_id: int, fr_idx: int, to_idx: int):
    if fr_idx>to_idx or fr_idx<0:
        raise ValueError(f"Practice word range is invalid: {fr_idx} to {to_idx}")
    wb=get_word_bank(s, wb_id)
    if not wb:
        raise ValueError(f"WordBank {wb_id} not found")
    max_idx=len(wb.bws)-1
    fr_idx=min(fr_idx, max_idx)
    to_idx=min(to_idx, max_idx)
    p=Practice(wb_id=wb_id, fr_idx=fr_idx, to_idx=to_idx, hard_only=0, assess_dt=date.today())
    s.add(p)

