import io
from typing import Callable, Tuple

def buf_pr()->Tuple[io.StringIO, Callable]:
    buf=io.StringIO()
    def pr2(*args):
        print(*args, file=buf)
    return (buf, pr2)

def indent_pr(pr):
    def pr2(*args):
        ls=list(args)
        ls[0]="\t"+ls[0]
        pr(*ls)
    return pr2
