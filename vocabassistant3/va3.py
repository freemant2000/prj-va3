from itertools import groupby
from typing import Sequence, Tuple
from . import db
from .models import Exercise, Sentence, WordAndMeaning, Sprint

def find_sentences(word: Sequence[str])->Sequence[Sentence]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select s.id, s.text from sentences s join snt_keywords k on s.id=k.snt_id 
            join word_defs wd on wd.id=k.wd_id
            where wd.word in %s group by s.id order by count(s.id) desc;
        """, (tuple(word),))
        rs=c.fetchall()
        snts=extract_sentences(rs)
        c.close()
    return snts

def load_keywords(snts: Sequence[Sentence])->None:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select k.snt_id, k.wd_id, wd.word, wm.p_of_s, wm.meaning from snt_keywords k join word_meanings wm on k.wd_id=wm.wd_id and k.wm_idx=wm.idx 
            join word_defs wd on wm.wd_id=wd.id
            where k.snt_id in %s order by k.snt_id, k.wd_id, k.wm_idx;
        """, (tuple([snt.id for snt in snts]),))
        rs=c.fetchall()
        extract_keywords(snts, rs)
        c.close()
    return snts

def extract_keywords(snts: Sequence[Sentence], rs: Sequence[Tuple])->None:
    d={snt.id:snt for snt in snts}
    gs=groupby(rs, lambda t: t[0])
    for (snt_id, sub_list) in gs:
        sub_list2=map(lambda t: t[1:], sub_list)
        d[snt_id].keywords=extract_words_and_meanings(sub_list2)
    return snts

def extract_sentences(rs: Sequence[Tuple])->Sequence[Sentence]:
    snts=[Sentence(id, text) for (id, text) in rs]
    return snts

def get_sprint(sp_id: int)->Sprint:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select s.id, s.start_dt, se.idx, se.e_id, e.dt from sprints s join sprint_exercise se on s.id=se.sp_id 
                join exercises e on e.id=se.e_id where s.id=%s order by s.id, se.idx;
        """, (sp_id,))
        rs=c.fetchall()
        sp=extract_sprint(rs)
        c.close()
    wd_ids=get_wd_in_sprint(sp_id)
    sp.wams=get_word_and_meanings(wd_ids)
    return sp

def extract_sprint(rs: Sequence[Tuple])->Sprint:
    sp=Sprint(rs[0][0], rs[0][1])
    for t in rs:
        sp.execs.append(Exercise(t[3], t[4]))
    return sp

def get_wd_in_sprint(sp_id: int)->Sequence[int]:
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

def add_word_and_meaning(wam: WordAndMeaning)->int:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("select nextval('word_seq')")
        id=c.fetchone()[0]
        c.execute("""
        insert into word_defs values(%s, %s)
        """, (id, wam.word))
        for (idx, (p_of_s, m)) in enumerate(wam.meanings):
            c.execute("insert into word_meanings values (%s, %s, %s, %s)", 
                      (id, idx, p_of_s, m))
        conn.commit()
        c.close()
        return id

def del_word_and_meaning(wd_id: int)->None:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        delete from word_meanings where wd_id=%s
        """, (wd_id,))
        c.execute("""
        delete from word_defs where id=%s
        """, (wd_id,))
        conn.commit()
        c.close()
        return id

def set_word_seq(v: int)->None:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select setval('word_seq', %s)
        """, (v,))
        c.close()
        return id

def get_similar_words(wd_prefix: str, limit: int=5)->Sequence[WordAndMeaning]:
    with db.connect() as conn:
        c=conn.cursor()
        c.execute("""
        select wd.id, word, p_of_s, meaning from word_defs wd join word_meanings wm on wd.id=wm.wd_id 
                  where wd.word like %s
                  order by word asc;
        """, (wd_prefix+"%",))
        rs=c.fetchmany(limit)
        ws=extract_words_and_meanings(rs)
        c.close()
        return ws

def get_wd_in_exercise(e_id: int)->Sequence[int]:
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
        select wd.id, word, p_of_s, meaning from word_defs wd join word_meanings wm on wd.id=wm.wd_id where wd.id in %s order by wd.id;
        """, (tuple(wd_ids),))
        rs=c.fetchall()
        ws=extract_words_and_meanings(rs)
        c.close()
        return ws

def extract_words_and_meanings(rs: Sequence)->Sequence[WordAndMeaning]:
    gs=groupby(rs, key=lambda t: (t[0], t[1]))
    ws=[]
    for ((id, w), ts) in gs:
        wam=WordAndMeaning(id, w)
        wam.meanings=[(p_of_s, m) for (id, w, p_of_s, m) in ts]
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