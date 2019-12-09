import socket
import sys
import os
from lib.medoo import Medoo
from lib.switch import Switch
import math


def salvaInCronologia(expression, result):
    db.insert('cronologia', {"expression": expression, "result": result})  # Inserisci nella tabella cronologia del
    # database l'espressione e il suo risultato


def Risposta(r):
    risultato = r  # Inizializzazione risultato
    clear = False  # Inizializzazione variabile
    operators = ['×', '÷', '+', '-', '√']  # Lista degli operatori
    while not clear:  # Finchè l'espressione non è stata analizzata tutta, allora...
        for operator in operators:  # ... per ogni operatore della lista operators ...
            trovato = r.find(operator)  # trova l'operatore nella stringa
            if trovato != -1:  # Se l'operatore è stato trovato...
                l = r.split(operator)  # Dividi la stringa in base all'operatore
                if operator == "-" and not l[0]:  # Se l'operatore è il - e se l'elemento in prima posizione
                    # dell'espressione è vuoto (ad esempio: -2-1 --> l = ["", "2", "1"]
                    del l[0]  # elimina quell'elemento
                    l[0] = -float(l[0])  # trasforma il nuovo primo elemento in un float (numero decimale) negativo
                for p, e in enumerate(l):  # Per ogni elemento (e la sua posizione) nell'espressione:
                    if type(e) == str:  # se l'elemento attuale è una stringa ...
                        e = e.replace(",",
                                      ".")  # ... sostituisci tutte le virgole con dei punti (per la trasformazione in stringa)
                    l[p] = float(e)  # Trasforma l'elemento in float
                with Switch(operator) as case:  # Switch (controlla che l'operatore sia uguale a...
                    if case(operators[0]):  # Primo operatore nella lista (multiply) + calcolo
                        risultato = 1
                        for x in l:
                            risultato = risultato * x
                    elif case(operators[1]):  # Secondo operatore nella lista (divide) + calcolo
                        risultato = l[0]
                        for p, x in enumerate(l):
                            if p == 0:
                                continue
                            risultato = risultato / x
                    elif case(operators[2]):  # Terzo operatore nella lista (plus) + calcolo
                        risultato = sum(l)
                    elif case(operators[3]):  # Quarto operatore nella lista (minus) + calcolo
                        for p, e in enumerate(l):
                            if p != 0 and float(e) > 0:
                                l[p] = -float(e)
                        risultato = sum(l)
                    elif case(operators[4]):  # Quinto operatore nella lista (square root) + calcolo
                        risultato = math.sqrt(float(l[1]))
                clear = True  # Quando il ciclo è concluso, imposta la variabile clear a True
                # (l'espressione è stata analizzata)
    salvaInCronologia(r, risultato)  # Salva nella cronologia l'espressione e il risultato
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
except OSError:  # otherwise
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
