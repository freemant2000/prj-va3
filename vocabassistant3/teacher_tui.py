from .db_base import open_session
from .practice import get_teacher

def teacher_tui():
    with open_session() as s:
        tch=get_teacher(s, 0)
        print("Students:")
        for stu in tch.stus:
            print(f"{stu.id} {stu.name}")
