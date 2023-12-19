from .teacher import get_teacher
from .db_base import open_session
from .user_prod_tui import get_current_user

def teacher_tui():
    with open_session() as s:
        tch=get_teacher(s, 0)
        print("Students:")
        for stu in tch.stus:
            print(f"{stu.id} {stu.name}")

def show_students():
    tch=get_current_user()
    for stu in tch.stus:
        print(f"{stu.id} {stu.name}")

