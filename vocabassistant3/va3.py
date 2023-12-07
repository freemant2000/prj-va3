from itertools import groupby
from typing import Sequence
import vocabassistant3.db as db
from vocabassistant3.word_meaning import WordAndMeaning

def find_sentences(word: Sequence[str])->Sequence[str]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("select s.text from sentences s join snt_keywords k on s.id=k.snt_id where k.word in %s group by s.id order by count(s.id) desc", (tuple(word),))
        rs=c.fetchall()
        c.close()
    return [r[0] for r in rs]

def get_wd_in_sprint(sp_id: int)->Sequence[str]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select distinct wd.id from 
            (select p.* from sprints s join sprint_practice sp on s.id=sp.sp_id join practices p on p.id=sp.p_id where s.id=%s) as p
                join bank_word bw on p.wb_id=bw.wb_id and bw.idx>=p.fr_idx and bw.idx<=p.to_idx
                join word_defs wd on bw.wd_id=wd.id;
        """, (sp_id,))
        rs=c.fetchall()
        c.close()
    return [r[0] for r in rs]

def get_similar_words(wd_prefix: str, limit: int=5)->Sequence[WordAndMeaning]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select word, p_of_s, meaning from word_defs wd join word_meanings wm on wd.id=wm.wd_id 
                  where wd.word like %s
                  order by word asc;
        """, (wd_prefix+"%",))
        rs=c.fetchmany(limit)
        ws=extract_words_and_meanings(rs)
        c.close()
        return ws

def get_wd_in_exercise(e_id: int)->Sequence[str]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select wd.* from exercises e join exercise_word_def ewd on e.id=ewd.e_id join word_defs wd on ewd.wd_id=wd.id where e.id=%s;
        """, (e_id,))
        rs=c.fetchall()
        c.close()
    return [r[0] for r in rs]

def get_word_and_meanings(wd_ids: Sequence[int])->Sequence[WordAndMeaning]:
     with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select word, p_of_s, meaning from word_defs wd join word_meanings wm on wd.id=wm.wd_id where wd.id in %s order by wd.id;
        """, (tuple(wd_ids),))
        rs=c.fetchall()
        ws=extract_words_and_meanings(rs)
        c.close()
        return ws

def extract_words_and_meanings(rs: Sequence)->Sequence[WordAndMeaning]:
    gs=groupby(rs, key=lambda t: t[0])
    ws=[]
    for (g, ms) in gs:
        wam=WordAndMeaning(g)
        wam.meanings=[(p_of_s, m) for (w, p_of_s, m) in ms]
        ws.append(wam)
    return ws

def get_snts_in_exercise(e_id: int)->Sequence[str]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select s.text from exercises e join exercise_snt es on e.id=es.e_id join sentences s on es.s_id=s.id where e.id=%s;
        """, (e_id,))
        rs=c.fetchall()
        c.close()
    return [r[0] for r in rs]