from disl import Disl
from vocabassistant3.config_reader import get_config_parser_from
from vocabassistant3 import db_base

cp=get_config_parser_from("va3-cfg-test.ini")
di=Disl()
di.add_raw_bean("db_url", cp.get("va3", "db_url"))
di.add_raw_bean("dbc", db_base.DBConnector())

