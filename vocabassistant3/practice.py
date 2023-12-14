from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, Date, Boolean
import datetime   
from .db_base import Base
from .word_bank import WordBank, BankWord
from typing import Sequence

class Practice(Base):
    __tablename__="practices"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    wb_id: Mapped[int]=mapped_column(Integer, ForeignKey("word_banks.id"))
    wb: Mapped[WordBank]=relationship("WordBank")
    fr_idx: Mapped[int]=mapped_column(Integer)
    to_idx: Mapped[int]=mapped_column(Integer)
    hard_only: Mapped[bool]=mapped_column(Boolean)
    assess_dt: Mapped[datetime.date]=mapped_column(Date)

    def get_bws(self)->Sequence[BankWord]:
        return self.wb.bws[self.fr_idx:self.to_idx+1]

