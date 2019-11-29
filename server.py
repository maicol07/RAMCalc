import socket
import sys
import math


def Risposta(r):
    risultato = r  # Inizializzazione risultato
    trova = r.find("+")
    trova1 = r.find("-")
    trova2 = r.find("×")
    trova3 = r.find("÷")
    trova4 = r.find("√")
    if trova != (-1):
        l = r.split("+")
        for p, e in enumerate(l):
            e = e.replace(",", ".")
            l[p] = float(e)
        risultato = sum(l)
    elif trova1 != (-1):
        l = r.split("-")
        for p, e in enumerate(l):
            e = e.replace(",", ".")
            l[p] = float(e)
            if p != 0:
                l[p] = -int(e)
        risultato = sum(l)
    elif trova2 != (-1):
        l = r.split("×")
        for p, e in enumerate(l):
            e = e.replace(",", ".")
            l[p] = float(e)
        risultato = 1
        for x in l:
            risultato = risultato * x
    elif trova3 != (-1):
        l = r.split("÷")
        for p, e in enumerate(l):
            e = e.replace(",", ".")
            l[p] = float(e)
        risultato = l[0]
        for p, x in enumerate(l):
            if p == 0:
                continue
            risultato = risultato / x
    elif trova4 != (-1):
        l = r.split("√")
        l[1] = l[1].replace(",", ".")
        risultato = math.sqrt(float(l[1]))
    return risultato


s = socket.socket()
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
try:
    if sys.argv[1] == "--localhost":
        ip = "127.0.0.1"
except IndexError:
    pass
s.bind((ip, 8888))
print(f"L'indirizzo ip di questo server è: {ip}")
s.listen(100)
conn, ip_client = s.accept()
while True:
    r = conn.recv(100)
    richiesta = r.decode()
    add = Risposta(richiesta)
    add = str(add)
    conn.send(add.encode())
