import socket
import math

def Risposta(r):
    trova=r.find("+")
    trova1 = r.find("-")
    trova2 = r.find("*")
    trova3 = r.find("/")
    trova4 = r.find("sqrt")
    if trova!=(-1):
        l=r.split("+")
        for e,p in enumerate(l):
            l[p]=int(e)
        risultato=sum(l)
    if trova1!=(-1):
        l=r.split("-")
        for e,p in enumerate(l):
            l[p]=int(e)
            if p != 0:
                l[p] = -int(e)
        risultato=sum(l)
    if trova2!=(-1):
        l=r.split("*")
        for e,p in enumerate(l):
            l[p]=int(e)
        risultato=1
        for x in l:
            risultato=risultato*x
    if trova3!=(-1):
        l=r.split("/")
        for e,p in enumerate(l):
            l[p]=int(e)
        risultato=l[0]
        for x in l:
            risultato=risultato/x
    if trova4!=(-1):
        l=r.split("sqrt")
        risultato=math.sqrt(int(l[1]))
    return risultato

s=socket.socket()
hostname=socket.gethostname()
ip=socket.gethostbyname(hostname)
s.bind((ip,8888))
print(f"L'indirizzo ip di questo server è: {ip}")
s.listen(100)
conn, ip_client=s.accept()
while True:
    r=conn.recv(100)
    richiesta=r.decode()
    add=Risposta(richiesta)
    add=str(add)
    conn.send(add.encode())






