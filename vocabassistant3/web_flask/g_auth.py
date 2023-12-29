from typing import Dict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_user_info(creds: Credentials)->Dict[str, str]:
    user_info_srv=build("oauth2", "v2", credentials=creds)
    user_info=user_info_srv.userinfo().get().execute()
    return user_info

def get_user_email(creds: Credentials)->str:
    user_info=get_user_info(creds)
    return user_info["email"]

