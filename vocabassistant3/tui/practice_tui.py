from ..db_base import open_session
from ..practice import get_practice

def toggle_hard_practice_tui():
    p_id=int(input("Input practice ID: "))
    with open_session() as s:
        prac=get_practice(s, p_id)
        if prac:
            prac.hard_only=not prac.hard_only
            s.commit()
            print("OK")
        else:
            print(f"Practice with ID {p_id} not found")

def show_wds_in_prac_tui():
    p_id=int(input("Input practice ID: "))
    with open_session() as s:
        prac=get_practice(s, p_id)
        if prac:
            for bw in prac.get_bws():
                print(f"{bw.get_full_word().ljust(20)}{bw.get_meanings()}")
        else:
            print(f"Practice with ID {p_id} not found")
