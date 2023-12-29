from .user_prod_flask import set_current_user
from flask import redirect

def login_fake_wp():
    try:
        set_current_user(1)
        return redirect("/teacher")
    except Exception as e:
        return "Error: "+str(e)
    
