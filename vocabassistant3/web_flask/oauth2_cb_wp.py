from flask import Flask, request
from disl import Disl
from ..db_base import open_session
from ..teacher import get_teacher_by_email
from .g_auth import get_user_email
from .g_oauth2 import GoogleOAuth2
from .user_prod_flask import set_current_user

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
        return "OK!"
    except Exception as e:
        return "Error: "+str(e)
