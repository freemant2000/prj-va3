from flask import redirect, render_template
from ..teacher import get_teacher
from ..db_base import open_session
from .user_prod_flask import get_current_user

def tch_land_wp():
    try:
        tch_id=get_current_user()
        if not tch_id:
            return redirect("/login")
        with open_session() as s:
            tch=get_teacher(s, tch_id)
            return render_template("tch_land_wp.html",  stus=tch.stus)
    except Exception as e:
        return "Error: "+str(e)

