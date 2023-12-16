
from typing import List


def get_lines_until_empty()->List[str]:
    lines=[]
    while True:
        line=input()
        if line:
            lines.append(line)
        else:
            return lines
            