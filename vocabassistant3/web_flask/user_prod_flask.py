from typing import Dict
from ..teacher import Teacher
from flask import session


def set_current_user(user_gmail: str):
    session["user"]=user_gmail

def get_current_user()->str: 
    return session.get("user", None)
