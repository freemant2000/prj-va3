from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import date

@dataclass
class WordAndMeaning:
    id: int
    word: str
    meanings: List[Tuple[str, str]]=field(default_factory=list)

    def add_meaning(self, p_of_s: str, meaning: str)->None:
        self.meanings.append((p_of_s, meaning))
    def get_display(self)->str:
        return self.word+"\t"+self.get_meanings()
    def get_meanings(self)->str:
        return u"、".join([f"{m}({p_of_s})" for (p_of_s, m) in self.meanings])

@dataclass
class Sentence:
    id: int
    text: str
    keywords: List[WordAndMeaning]=field(default_factory=list)

@dataclass
class Exercise:
    id: int
    dt: date
    wams: List[WordAndMeaning]=field(default_factory=list)
    snts: List[Sentence]=field(default_factory=list)

    def add_word(self, wam: WordAndMeaning)->None:
        self.wams.append(wam)
    def add_sentence(self, snt: Sentence)->None:
        self.snts.append(snt)

@dataclass
class Sprint:
    id: int
    start_dt: date
    wams: List[WordAndMeaning]=field(default_factory=list)
    execs: List[Exercise]=field(default_factory=list)

