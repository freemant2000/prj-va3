from .user_prod_tui import get_current_user

def show_students_tui():
    tch=get_current_user()
    for stu in tch.stus:
        print(f"{stu.id} {stu.name}")

