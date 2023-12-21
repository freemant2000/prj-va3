from ..teacher import Teacher

current_user:Teacher=None

def set_current_user(user: Teacher):
    global current_user
    current_user=user

def get_current_user()->Teacher: 
    return current_user
