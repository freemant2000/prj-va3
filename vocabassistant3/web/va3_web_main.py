import justpy as jp
from . import stud_main_wp, exec_wp, login_wp, sprint_wp

jp.WebPage.tailwind=False
jp.justpy(stud_main_wp.stud_main_wp)