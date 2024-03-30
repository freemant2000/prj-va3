from random import shuffle
from flask import render_template
from ..db_base import open_session
from ..sprint import Exercise, get_exec

def exec_pub_wp(e_id):
    try:
        with open_session() as s:
            exec=get_exec(s, e_id)
            if not exec:
                raise ValueError(f"Exercise {e_id} not found")
            shuffle(exec.ews)
            return render_template("exec_pub_wp.html", exec=exec)
    except Exception as e:
        return "Error: "+str(e)
