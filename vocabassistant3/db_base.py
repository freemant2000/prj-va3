from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, text


class Base(DeclarativeBase):
    pass

def open_session()->Session:
    eng=create_engine(f"postgresql://dba:abc123@localhost/va3", echo=True)
    s=Session(eng)
    return s

def set_seq_val(s: Session, seq_name: str, val: int):
    s.execute(text(f"select setval(:sn, :v)"), {"sn": seq_name, "v": val})
