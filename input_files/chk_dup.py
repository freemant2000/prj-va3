from subprocess import call, DEVNULL

f=open("vocab-doraemon-new")
for e in f:
    if e.startswith("\t"):
        continue
    e=e.strip()
    cmd="grep '"+e+"' vocab-doraemon-*-L2.txt"
    p=call(cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL)
    if p==1:
        print(e)
f.close()
