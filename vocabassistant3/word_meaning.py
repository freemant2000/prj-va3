from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class WordAndMeaning:
    word: str
    meanings=[]

    def add_meaning(self, p_of_s: str, meaning: str)->None:
        self.meanings.append((p_of_s, meaning))
    def get_display(self)->str:
        return self.word+"\t"+self.get_meanings()
    def get_meanings(self)->str:
        return u"、".join([f"{m}({p_of_s})" for (p_of_s, m) in self.meanings])
