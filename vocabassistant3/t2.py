from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session, joinedload  
from .m2 import WordDef, WordMeaning

eng=create_engine(f"postgresql://dba:abc123@localhost/va3")
with Session(eng) as s:
  # q=select(WordDef).where(WordDef.id==0).options(joinedload(WordDef.meanings))
  q=select(WordDef).where(WordDef.meanings.any(WordMeaning.p_of_s=='v')).options(joinedload(WordDef.meanings))
  r=s.scalars(q)
  for wd in r.unique().all():
    print(wd.word)
    for m in wd.meanings:
      print("\t"+m.meaning)
