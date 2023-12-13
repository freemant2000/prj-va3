from typing import Sequence
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload
from .models import Exercise, Practice, Sentence, Sprint, WordBank, WordDef, WordMeaning


def open_session():
  eng=create_engine(f"postgresql://dba:abc123@localhost/va3", echo=True)
  s=Session(eng)
  return s

def get_word_defs(s: Session, wd_ids: Sequence[int])->Sequence[WordDef]:
  q=select(WordDef).where(WordDef.id.in_(wd_ids)).options(joinedload(WordDef.meanings)) \
      .order_by(WordDef.id.asc())
  r=s.scalars(q)
  wds=r.unique().all()
  return wds

def del_word_def(s: Session, wd_id: int)->None:
  q=select(WordDef).where(WordDef.id==(wd_id))
  r=s.scalars(q)
  wd=r.unique().first()
  s.delete(wd)

def get_similar_words(s: Session, pref: str, limit:int=5)->Sequence[WordDef]:
  return get_words_by_pattern(s, pref+"%", limit)

def get_word_def(s: Session, word: str, limit:int=5)->Sequence[WordDef]:
  return get_words_by_pattern(s, word, limit)

def get_words_by_pattern(s: Session, pattern: str, limit:int=5)->Sequence[WordDef]:
  q=select(WordDef).where(WordDef.word.like(pattern)).options(joinedload(WordDef.meanings)) \
      .order_by(WordDef.id.asc())
  r=s.scalars(q)
  wds=r.unique().all()
  return wds

def get_snts(s: Session, words: Sequence[str])->Sequence[Sentence]:
  q=select(Sentence).where(Sentence.keywords.any(WordMeaning.wd.has(WordDef.word.in_(words)))) \
      .options(joinedload(Sentence.keywords).joinedload(WordMeaning.wd)) \
      .order_by(Sentence.id.asc())
  r=s.scalars(q)
  return r.unique().all()

def get_exec(s: Session, e_id: int)->Exercise:
  q=select(Exercise).where(Exercise.id==e_id).options(joinedload(Exercise.wds)).options(joinedload(Exercise.snts).joinedload(Sentence.keywords))
  r=s.scalars(q)
  exec=r.unique().first()
  return exec

def get_sprint(s: Session, sp_id: int)->Sprint:
  q=select(Sprint).where(Sprint.id==sp_id) \
    .options(joinedload(Sprint.pracs).joinedload(Practice.wb).joinedload(WordBank.wds).joinedload(WordDef.meanings)) \
    .options(joinedload(Sprint.execs).joinedload(Exercise.wds).joinedload(WordDef.meanings))
  r=s.scalars(q)
  sp=r.unique().first()
  return sp


