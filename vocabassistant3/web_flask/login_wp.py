from .main_disl import di
from flask import redirect

def login_wp():
    try:
        goa=di.get_wired_bean("goa")
        url=goa.get_redirect_uri()
        return redirect(url)
    except Exception as e:
        return "Error: "+str(e)
    
