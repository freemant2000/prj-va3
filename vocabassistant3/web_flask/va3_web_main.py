from flask import Flask, render_template

from .pronounce import pronounce
from .stud_wp import stud_main_wp
from .sprint_wp import sprint_wp
from .exec_wp import exec_wp
from .exec_pub_wp import exec_pub_wp
from .tch_land_wp import tch_land_wp
from .oauth2_cb_wp import oauth2_cb
from .login_wp import login_wp
from .main_disl import di

app=Flask(__name__)
app.secret_key=di.get_wired_bean("session_encrpt_key")
app.add_url_rule("/stus/<int:stu_id>", view_func=stud_main_wp)
app.add_url_rule("/sprints/<int:sp_id>", view_func=sprint_wp)
app.add_url_rule("/execs/<int:e_id>", view_func=exec_wp)
app.add_url_rule("/execs/pub/<int:e_id>", view_func=exec_pub_wp)
app.add_url_rule("/teacher", view_func=tch_land_wp)
app.add_url_rule("/login", view_func=login_wp)
app.add_url_rule("/oauth2_callback", view_func=oauth2_cb)
app.add_url_rule("/pronounce/<int:wd_id>", view_func=lambda wd_id: pronounce(di.get_wired_bean("temp_dir", wd_id)))

@app.route("/")
def home_page():
    return render_template("va3_main_wp.html")
    
