from flask import Flask, request
from disl import Disl
from ..config_reader import get_config_parser
from ..db_base import open_session
from ..teacher import get_teacher_by_email
from .g_auth import get_user_email
from .g_oauth2 import GoogleOAuth2
from .user_prod_flask import set_current_user
from .stud_wp import stud_main_wp
from .sprint_wp import sprint_wp
from .exec_wp import exec_wp
from .. import db_base

app=Flask(__name__)
app.secret_key=cp.get("va3", "session_encrpt_key")
app.add_url_rule("/stus/<int:stu_id>", view_func=stud_main_wp)
app.add_url_rule("/sprints/<int:sp_id>", view_func=sprint_wp)
app.add_url_rule("/execs/<int:e_id>", view_func=exec_wp)
cp=get_config_parser()
di=Disl()
di.add_raw_bean("db_url", cp.get("va3", "db_url"))
di.add_raw_bean("client_secret_file", cp.get("va3", "client_secret_file"))
di.add_raw_bean("redirect_uri", cp.get("va3", "redirect_uri"))
di.add_raw_bean("goa", GoogleOAuth2())
di.add_raw_bean("dbc", db_base.DBConnector())
db_base.dbc=di.get_wired_bean("dbc")

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
            set_current_user(tch.id)
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

