import socket
import sys
import os
from lib.medoo import Medoo
from lib.switch import Switch
import math


def salvaInCronologia(expression, result):
    db.insert(
        'cronologia',
        {"expression": expression, "result": result}
    )


def Risposta(r):
    risultato = r  # Inizializzazione risultato
    clear = False
    operators = ['×', '÷', '+', '-', '√']
    while not clear:
        for operator in operators:
            trovato = r.find(operator)
            if trovato != -1:
                l = r.split(operator)
                if operator == "-":
                    if not l[0]:
                        del l[0]
                        l[0] = -float(l[0])
                for p, e in enumerate(l):
                    if type(e) == str:
                        e = e.replace(",", ".")
                    l[p] = float(e)
                with Switch(operator) as case:
                    if case(operators[0]):  # multiply
                        risultato = 1
                        for x in l:
                            risultato = risultato * x
                    elif case(operators[1]):  # divide
                        risultato = l[0]
                        for p, x in enumerate(l):
                            if p == 0:
                                continue
                            risultato = risultato / x
                    elif case(operators[2]):  # sum
                        risultato = sum(l)
                    elif case(operators[3]):  # minus
                        for p, e in enumerate(l):
                            if p != 0 and float(e) > 0:
                                l[p] = -float(e)
                        risultato = sum(l)
                    elif case(operators[4]):  # square root
                        risultato = math.sqrt(float(l[1]))
                clear = True
    salvaInCronologia(r, risultato)
    return risultato


# Apertura database (viene creato se non esiste già il file) e creazione tabelle se non esistono già
if not (os.path.exists(os.path.expanduser('~/Documents/RAMCalc'))):
    os.makedirs(os.path.expanduser('~/Documents/RAMCalc'))
    open(os.path.expanduser('~/Documents/RAMCalc/db.db'), "w").close()  # Creazione file database
db = Medoo('sqlite', database=os.path.expanduser('~/Documents/RAMCalc/db.db'))
query = open("tables.sql")
db.connection.executescript(query.read())
query.close()

s = socket.socket()
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
try:
    if sys.argv[1] == "--localhost":
        ip = "127.0.0.1"
except IndexError:
    pass
# Check if a server already exists
try:
    s.bind((ip, 8888))
except OSError:
    exit()
print("L'indirizzo ip di questo server è: {}".format(ip))
s.listen(100)
conn, ip_client = s.accept()
while True:
    r = conn.recv(100)
    richiesta = r.decode()
    add = Risposta(richiesta)
    add = str(add)
    conn.send(add.encode())
