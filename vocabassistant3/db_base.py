from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, text


class Base(DeclarativeBase):
    pass

dbname="va3_test"

def set_dbname(dbn: str):
    global dbname
    dbname=dbn
    
def open_session()->Session:
    eng=create_engine(f"mysql+pymysql://dba:abc123@localhost/{dbname}", echo=False)
    s=Session(eng)
    return s

def set_seq_val(s: Session, tbl_name: str):
    s.execute(text(f"alter table {tbl_name} auto_increment=1"))

