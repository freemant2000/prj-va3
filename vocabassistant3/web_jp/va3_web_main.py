import justpy as jp
from . import exec_wp, login_wp, sprint_wp, stud_wp

jp.WebPage.tailwind=False
jp.justpy(stud_wp.stud_main_wp)