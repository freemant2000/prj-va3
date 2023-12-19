from vocabassistant3.student_tui import show_student_tui
from vocabassistant3.word_bank_tui import show_word_banks_tui
from .teacher_tui import show_students_tui
from .db_base import open_session
from .teacher import get_teacher
from .user_prod_tui import set_current_user

def show_help():
    for cmd, (descp, func) in cmds.items():
        print(f"{cmd}: {descp}")

cmds={"help": ("Show available commands", show_help), 
      "sss": ("Show Students", show_students_tui),
      "ss": ("Show Student", show_student_tui),
      "swbs": ("Show Word Banks", show_word_banks_tui)}

def main_tui():
    log_in()
    while True:
        cmd=input("Input command: ")
        if cmd in cmds:
            try:
                cmds[cmd][1]()
            except Exception as e:
                print("Error: "+str(e))
        else:
            print("Command unknown. Type help to see all commands.")

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