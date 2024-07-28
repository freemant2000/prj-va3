from .user_prod_tui import get_current_user

def show_students_tui():
    tch=get_current_user()
    stus=sorted(tch.stus, key=lambda s: s.id)
    for stu in stus:
        print(f"{stu.id} {stu.name}")

