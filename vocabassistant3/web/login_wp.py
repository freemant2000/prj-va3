from typing import Dict
import justpy as jp
from ..db_base import open_session
from ..teacher import get_teacher
from .user_prod_web import set_current_user

def on_login(c, ev: Dict):
    try:
        with open_session() as s:
            tch=get_teacher(s, 1)
            set_current_user(ev.session_id, tch)
    except Exception as e:
        wp=jp.WebPage()
        jp.H3(text="Error: "+str(e), a=wp)
        ev.page.redirect(wp)

@jp.SetRoute("/login")
def login_wp():
    wp=jp.WebPage()
    try:
        jp.Button(text="Login", click=on_login, a=wp)
    except Exception as e:
        jp.H3(text="Error: "+str(e), a=wp)
    return wp
