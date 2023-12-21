from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, text


class Base(DeclarativeBase):
    pass

def open_session()->Session:
    eng=create_engine(f"mysql+pymysql://dba:abc123@localhost/va3_test", echo=False)
    s=Session(eng)
    return s

def set_seq_val(s: Session, tbl_name: str):
    s.execute(text(f"alter table {tbl_name} auto_increment=1"))

