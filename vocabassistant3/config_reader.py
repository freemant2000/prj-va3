from configparser import ConfigParser
from os import environ

def get_config_parser()->ConfigParser:
    cfg_path=environ.get("va3_cfg")
    if not cfg_path:
        cfg_path="va3-cfg-test.ini"  # in current dir
    return get_config_parser_from(cfg_path)

def get_config_parser_from(cfg_path: str)->ConfigParser:
    cp=ConfigParser()
    cp.read(cfg_path)
    return cp