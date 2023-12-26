from .cmd_handler import CmdHandler
from .word_defs_tui import word_defs_tui
from .sentence_tui import snts_tui
from .student_tui import show_student_tui
from .word_bank_tui import word_banks_tui
from .teacher_tui import show_students_tui
from .user_prod_tui import set_current_user
from ..db_base import open_session, set_dbname
from ..teacher import get_teacher
from argparse import ArgumentParser

def main_tui():
    ap=ArgumentParser()
    ap.add_argument("-d", "--dbname", default="va3_test")
    args=ap.parse_args()
    set_dbname(args.dbname)
    log_in()
    cmds={"ss": ("Show students", show_students_tui),
        "s": ("Work on a student", show_student_tui),
        "wbs": ("Work on the word banks", word_banks_tui),
        "snts": ("Work on the sentences", snts_tui),
        "wds": ("Work on the word defs", word_defs_tui)}
    ch=CmdHandler(">", cmds)
    ch.main_loop()

def log_in():
    while True:
        try:
            tch_id=int(input("Input teacher ID: "))
            with open_session() as s:
                tch=get_teacher(s, tch_id)
                set_current_user(tch)
                return
        except Exception as e:
            print("Error: "+str(e))

if __name__=="__main__":
    main_tui()