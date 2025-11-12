from subprocess import call, DEVNULL

f=open("vocab-doraemon-11-L2")
for e in f:
    e=e.strip()
    cmd="grep "+e+" vocab-doraemon-*-L2.txt"
    p=call(cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL)
    if p==1:
        print(e)
f.close()
