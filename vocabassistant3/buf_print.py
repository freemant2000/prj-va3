import io
from typing import Callable, Tuple

def buf_pr()->Tuple[io.StringIO, Callable]:
    buf=io.StringIO()
    def pr2(*args):
        print(*args, file=buf)
    return (buf, pr2)
