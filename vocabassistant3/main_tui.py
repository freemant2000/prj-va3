from .cmd_handler import CmdHandler
from .student_tui import show_student_tui
from .word_bank_tui import word_banks_tui
from .teacher_tui import show_students_tui
from .db_base import open_session
from .teacher import get_teacher
from .user_prod_tui import set_current_user


def main_tui():
    log_in()
    cmds={"sss": ("Show Students", show_students_tui),
        "ss": ("Show Student", show_student_tui),
        "wb": ("Word Banks", word_banks_tui)}
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