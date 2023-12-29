from test_disl import di
from sqlalchemy.orm import Session

dbc=di.get_wired_bean("dbc")

def open_session()->Session:
    return dbc.open_session()
