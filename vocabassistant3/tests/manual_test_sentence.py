from vocabassistant3.sentence import SentenceDraft, add_snt_draft
from vocabassistant3.db_base import open_session
from vocabassistant3.word_def import WordMeaning

with open_session() as s:
    sd=SentenceDraft(text="這個山谷有巨大的有角的松鼠。", 
                   keywords=["valley", "squirrel", "horn"],
                   kw_meanings={
                       "valley": WordMeaning(wd_id=5, idx=0, p_of_s="n", meaning="山谷"),
                       "squirrel": WordMeaning(wd_id=4, idx=0, p_of_s="n", meaning="松鼠"),
                       "horn": WordMeaning(wd_id=10, idx=0, p_of_s="n", meaning="（動物）角")})
    add_snt_draft(s, sd)
    s.commit()
