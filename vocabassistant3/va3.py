from typing import Sequence
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload
from .models import Exercise, Practice, Sentence, Sprint, WordBank, WordDef, WordMeaning, BankWord, ExeciseWord


def get_snts(s: Session, words: Sequence[str])->Sequence[Sentence]:
  q=select(Sentence).where(Sentence.keywords.any(WordMeaning.wd.has(WordDef.word.in_(words)))) \
      .options(joinedload(Sentence.keywords).joinedload(WordMeaning.wd)) \
      .order_by(Sentence.id.asc())
  r=s.scalars(q)
  return r.unique().all()

def get_exec(s: Session, e_id: int)->Exercise:
  q=select(Exercise).where(Exercise.id==e_id) \
    .options(joinedload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Exercise.snts).joinedload(Sentence.keywords))
  r=s.scalars(q)
  exec=r.unique().first()
  return exec

def get_word_bank(s: Session, wb_id: int)->WordBank:
  q=select(WordBank).where(WordBank.id==wb_id) \
    .options(joinedload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings))
  r=s.scalars(q)
  exec=r.unique().first()
  return exec

def get_sprint(s: Session, sp_id: int)->Sprint:
  q=select(Sprint).where(Sprint.id==sp_id) \
    .options(joinedload(Sprint.pracs).joinedload(Practice.wb).joinedload(WordBank.bws).joinedload(BankWord.wd).joinedload(WordDef.meanings)) \
    .options(joinedload(Sprint.execs).joinedload(Exercise.ews).joinedload(ExeciseWord.wd).joinedload(WordDef.meanings))
  r=s.scalars(q)
  sp=r.unique().first()
  return sp


