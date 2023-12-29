from flask import Flask, request
from disl import Disl
from ..db_base import open_session
from ..teacher import get_teacher_by_email
from .g_auth import get_user_email
from .g_oauth2 import GoogleOAuth2
from .user_prod_flask import set_current_user

app=Flask(__name__)
app.secret_key="kvgfi88lmb993gf09823923en2r3"
di=Disl()
di.add_raw_bean("client_secret_file", "/home/kent/prj-va3/client-secret.json")
di.add_raw_bean("redirect_uri", "http://localhost:8000/oauth2_callback")
di.add_raw_bean("goa", GoogleOAuth2())

@app.route("/oauth2_callback")
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
            set_current_user(tch.gmail)
        return "OK!"
    except Exception as e:
        return "Error: "+str(e)

@app.route("/login")
def login_page():
    try:
        goa=di.get_wired_bean("goa")
        url=goa.get_redirect_uri()
        return app.redirect(url)
    except Exception as e:
        return "Error: "+str(e)
    
@app.route("/")
def home_page():
    return "<p>Hi</p>"

