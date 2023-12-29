from flask import session

def set_current_user(user_id: int):
    session["user"]=user_id

def get_current_user()->int: 
    return session.get("user", None)
