from flask import request, redirect
from ..db_base import open_session
from ..teacher import get_teacher_by_email
from .g_auth import get_user_email
from .user_prod_flask import set_current_user
from .main_disl import di

def oauth2_cb():
    try:
        code=request.args["code"]
        goa=di.get_wired_bean("goa")
        creds=goa.get_creds_with_code(code)
        email=get_user_email(creds)
        with open_session() as s:
            tch=get_teacher_by_email(s, email)
            if not tch:
                raise ValueError("Login failed")
            set_current_user(tch.id)
        return redirect("/teacher")
    except Exception as e:
        return "Error: "+str(e)
