
from typing import List


def get_lines_until_empty()->List[str]:
    lines=[]
    while True:
        line=input()
        if line:
            lines.append(line)
        else:
            return lines

def indent_pr(pr):
    def pr2(*args):
        ls=list(args)
        ls[0]="\t"+ls[0]
        pr(*ls)
    return pr2
