from typing import Dict
from ..teacher import Teacher

logged_in_users:Dict[str, Teacher]={}

def set_current_user(session_id: str, user: Teacher):
    logged_in_users[session_id]=user

def get_current_user(session_id: str)->Teacher: 
    user=logged_in_users.get(session_id, None)
    return user
