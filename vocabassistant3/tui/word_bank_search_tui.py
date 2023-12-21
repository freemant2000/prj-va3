from .cmd_handler import CmdHandler, ExitException
from ..word_bank import WordBank, find_word_banks, get_word_bank
from ..db_base import open_session

wb_selected: WordBank=None

def search_word_bank_tui()->WordBank:
    cmds={"s": ("Perform a keyword search for Word Banks", search_word_banks),
          "c": ("Choose a Word Bank", choose_word_bank)}
    ch=CmdHandler(f"find-wb>", cmds)
    ch.main_loop()
    return wb_selected

def search_word_banks():
    kw=input("Input a keyword: ")
    with open_session() as s:
        wbs=find_word_banks(s, kw)
    for wb in wbs:
        print(f"{wb.id} {wb.name} {wb.get_no_words()} words")

def choose_word_bank():
    global wb_selected
    wb_id=int(input("Input a WordBank ID: "))
    with open_session() as s:
        wb=get_word_bank(s, wb_id)
        wb_selected=wb
        raise ExitException()
