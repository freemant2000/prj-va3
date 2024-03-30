from disl import Disl

from .g_oauth2 import GoogleOAuth2
from .. import db_base
from ..config_reader import get_config_parser

cp=get_config_parser()
di=Disl()
di.add_raw_bean("session_encrpt_key", cp.get("va3", "session_encrpt_key"))
di.add_raw_bean("db_url", cp.get("va3", "db_url"))
di.add_raw_bean("client_secret_file", cp.get("va3", "client_secret_file"))
di.add_raw_bean("redirect_uri", cp.get("va3", "redirect_uri"))
di.add_raw_bean("goa", GoogleOAuth2())
di.add_raw_bean("dbc", db_base.DBConnector())
di.add_raw_bean("temp_dir", cp.get("va3", "temp_dir"))
db_base.dbc=di.get_wired_bean("dbc")
