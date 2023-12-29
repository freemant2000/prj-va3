from google_auth_oauthlib.flow import Flow
from flask import Flask, request, session
from googleapiclient.discovery import build

from .g_oauth2 import GoogleOAuth2, get_redirect_uri, handle_code

app=Flask(__name__)

goa=GoogleOAuth2(
    client_secret_file="/home/kent/prj-va3/client-secret.json",
    redirect_uri="http://localhost:8000/oauth2_callback")

@app.route("/oauth2_callback")
def oauth2_cb():
    code=request.args["code"]
    creds=goa.get_creds_with_code(code)
    user_info_srv=build("oauth2", "v2", credentials=creds)
    user_info=user_info_srv.userinfo().get().execute()
    print(user_info)
    return "OK!"

@app.route("/login")
def login_page():
    url=goa.get_redirect_uri()
    return app.redirect(url)

@app.route("/")
def home_page():
    return "<p>Hi</p>"

@app.route("/p2")
def page2():
    return "<p>Hello</p>"