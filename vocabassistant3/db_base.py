from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, text
from disl import Inject

class Base(DeclarativeBase):
    pass

class DBConnector:
    def __init__(self) -> None:
        self.db_url=Inject()
    def open_session(self)->Session:
        eng=create_engine(self.db_url, echo=False)
        s=Session(eng)
        return s
dbc=None

def open_session()->Session:
    return dbc.open_session()

def set_seq_val(s: Session, tbl_name: str):
    s.execute(text(f"alter table {tbl_name} auto_increment=1"))

