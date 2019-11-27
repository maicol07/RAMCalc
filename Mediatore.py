#Massari Riccardo
import socket
s=socket.socket()
def invia (dati,ip):
    s.connect((ip,888))
    datien=dati.encode()
    s.send(datien)

def chiuditutto():
    s.close()

def ricevi():
    risultato=s.recv(50)
    risultatode=risultato.decode()
    return risultatode
