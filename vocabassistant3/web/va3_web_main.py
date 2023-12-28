import justpy as jp
from . import exec_wp, login_wp
from .sprint_wp import sprint_wp

jp.WebPage.tailwind=False
jp.justpy(sprint_wp)