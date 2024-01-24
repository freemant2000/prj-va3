from ..sentence import Sentence
from ..word_def import WordDef, WordMeaning
from ..sprint import Exercise, ExeciseWord

def sample_data():
    exec=Exercise(id=0)
    exec.ews.append(ExeciseWord(
                    wd=WordDef(id=0, word="hand", 
                                meanings=[WordMeaning(meaning="手", p_of_s="n"),
                                          WordMeaning(meaning="遞", p_of_s="v")]), m_indice="0,1"))
    exec.ews.append(ExeciseWord(
                    wd=WordDef(id=1, word="drink", 
                                meanings=[WordMeaning(meaning="喝", p_of_s="v"),
                                          WordMeaning(meaning="飲品", p_of_s="n")]), m_indice="1"))
    exec.snts.append(Sentence(id=0, text="他喝了水"))
    exec.snts.append(Sentence(id=1, text="他的手很大"))
    return exec

print(sample_data())
