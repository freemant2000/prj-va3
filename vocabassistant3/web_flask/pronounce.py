from flask import send_file
from ..tts_engine import launch_speak
from ..word_def import get_word_def_by_id
from ..db_base import open_session
from tempfile import gettempdir
from os import path

def pronounce(wd_id: int):
    try:
        with open_session() as s:
            wd=get_word_def_by_id(s, wd_id)
            dir=gettempdir()
            p=path.join(dir, f"va3-pron-{wd_id}.mp3")
            launch_speak(wd.word, p)
            return send_file(p, max_age=3600)
    except Exception as e:
        return "Error: "+str(e)
