from vocabassistant3.sentence import Sentence, SentenceDraft
from vocabassistant3.db_base import open_session
from vocabassistant3.sprint import ExerciseDraft, get_sprint, show_sprint, refine_exec_draft, show_exec_draft
from vocabassistant3.word_def import WordMeaning

with open_session() as s:
  sp=get_sprint(s, 0)
  ed=ExerciseDraft()
  ed.words.extend(["mountain", "river", "flow", "trunk", "wise"])
  ed.snt_texts=["這個山很陡峭。", "這個山上的岩石很堅硬。", "這個山谷有巨大的有角的松鼠。"]
  ed.old_snts["這個山很陡峭。"]=Sentence(id=0, text="這個山很陡峭。", 
                                keywords=[WordMeaning(wd_id=0, idx=0, p_of_s="adj", meaning="陡峭（斜）的"),
                                          WordMeaning(wd_id=1, idx=0, p_of_s="n", meaning="山")])
  ed.new_snt_drafts["這個山谷有巨大的有角的松鼠。"]=SentenceDraft(text="這個山谷有巨大的有角的松鼠。", 
                                keywords=["valley", "large", "squirrel", "horn"],
                                kw_meanings={"valley": WordMeaning(wd_id=5, idx=0, p_of_s="n", meaning="山谷")})
  refine_exec_draft(s, sp, ed)  
  show_exec_draft(ed)

