from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass

def open_session():
  eng=create_engine(f"postgresql://dba:abc123@localhost/va3", echo=False)
  s=Session(eng)
  return s
