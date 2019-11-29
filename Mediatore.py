#Massari Riccardo
import socket
import tkinter.messagebox as tkmb
s=socket.socket()


def crea_socket():
    s = socket.socket()
    return s


def invia(dati):
    if not dati:
        return
    datien=dati.encode()
    try:
        s.send(datien)
    except OSError:
        tkmb.showerror(title="Connessione chiusa",
                       message="La connessione al server si è interrotta. Ricollegati al socket da Impostazioni --> "
                               "Collega ad un server")


def connetti(ip):
    global s
    try:
        s.connect((ip, 8888))
    except OSError:
        s = crea_socket()
        connetti(ip)

def chiuditutto():
    s.close()

def ricevi():
    try:
        risultato = s.recv(50)
    except OSError:
        tkmb.showerror(title="Connessione chiusa",
                       message="La connessione al server si è interrotta. Ricollegati al socket da Impostazioni --> "
                               "Collega ad un server")
        return
    risultatode=risultato.decode()
    return risultatode
