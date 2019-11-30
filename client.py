'''
# RAMCalc
###### A simple calculator

Questo programma interpreta dati passati da un computer
e li elabora in operazioni matematiche, restituendoli ad un altro computer.

Permette le seguenti operazioni:
- Addizione
- Sottrazione
- Moltiplicazione
- Divisione
- Radice quadrata

**ATTENZIONE: Per mancanza di tempo, non è possibile inserire espressioni
all'interno del calcolatore (Funzionalità non realizzata)**

È possibile immettere i numeri e i vari operatori tramite i pulsanti della
GUI o attraverso la tastiera fisica del dispositivo (in questo caso, quando
si preme `INVIO` si otterrà lo stesso risultato della pressione del tasto `=`)

Altre funzioni dell'interfaccia grafica incorporata includono:
- Selezione tema della GUI
- Selezione del carattere utilizzato nella GUI
- Collegamento ad un altro server o riconnessione allo stesso
- Finestra informazioni su RAMCalc

Contributi dei singoli:
- maicol07 (_Maicol Battistini_):
    - GUI
    - Impostazioni (Temi, carattere)
    - Opzione collegamento ad un server differente
    - Cronologia
    - Finestra informazioni
    - Design del software
    - Integrazione librerie esterne
    - Interazione con il database per il salvataggio del tema, del carattere e della cronologia
- RichiMassa1 (_Riccardo Massari_): Client (connessione iniziale con il server
ed invio dati), Server (alcune operazioni)
- alecoma (_Alessia Comandini_): Server
'''
import sys
import os

sys.path.insert(0, 'lib')
# ========== CLASSI ========== #
from src.common import import_pil

import_pil()

from tkinter import *
from tkinter.ttk import *
from lib.ttkSimpleDialog import ttkSimpleDialog
from lib.medoo import Medoo

import Mediatore
from modules.settings import *
from modules.Cronologia import cronologia

# Apertura database (viene creato se non esiste già il file) e creazione tabelle se non esistono già
if not (os.path.exists(os.path.expanduser('~/Documents/RAMCalc'))):
    os.makedirs(os.path.expanduser('~/Documents/RAMCalc'))
    open(os.path.expanduser('~/Documents/RAMCalc/db.db'), "w").close()  # Creazione file database
db = Medoo('sqlite', database=os.path.expanduser('~/Documents/RAMCalc/db.db'))
query = open("tables.sql")
db.connection.executescript(query.read())
query.close()


def sendToServer(entry):
    data = entry.get()
    if not data:
        return
    Mediatore.invia(data)
    risp = Mediatore.ricevi()
    writeToEntry(risp, delete=True, reenable_others=True)


def writeToEntry(text, delete=False, pressed=False, disable_others=False, reenable_others=False):
    if delete:
        e.delete(0, END)
    if text in operators + ['√'] and str(btns[text]['state']) == 'disabled':
        return 'break'
    e.insert(END, text)
    e.focus_set()
    if disable_others:
        for t, btn in btns.items():
            if t == text or btn['text'] == text:
                continue
            btn.configure(state=DISABLED)
        if '√' in e.get():
            btns['√'].configure(state=DISABLED)
    if reenable_others:
        l = []
        for i in operators + ['√']:
            if i in e.get()[:-1]:
                l.append(i)
        for t, btn in btns.items():
            if not btn['text'] in l and l or '√' in e.get()[:-1]:
                continue
            btn.configure(state=NORMAL)
    if pressed:
        return "break"


def ip(initialvalue=""):
    Mediatore.chiuditutto()
    ip = ttkSimpleDialog.askstring("Indirizzo IP",
                                   "Digita l'indirizzo IP del server. Se il server è sul tuo computer digita "
                                   "localhost o 127.0.0.1.\nSe premi Annulla o non immetti nulla verrà avviato il "
                                   "server interno.",
                                   parent=w, initialvalue=initialvalue)
    process = None
    if ip is None or ip == "":
        import subprocess
        if sys.version_info.minor > 5:
            cmd = 'python'
        else:
            cmd = 'py'
        process = subprocess.Popen("{} server.py --localhost".format(cmd), shell=True, stdout=subprocess.DEVNULL)
        ip = "127.0.0.1"
    Mediatore.connetti(ip)
    return ip, process


def buttons(frame, l, column_limit=3):
    """
    Generates and places common buttons

    :param column_limit:
    :param frame:
    :param l:
    :return:
    """
    tk_elements = {}
    r = 0
    c = 0
    if type(l) == list:
        cyclic = l
    else:
        cyclic = l.keys()
    for i in cyclic:
        if type(l) == list:
            text = i
        else:
            text = l[i]
        if text not in operators + ['√']:
            disable = False
        else:
            disable = True
        b = Button(frame, text=text, command=lambda text=text: writeToEntry(text, disable_others=disable))
        if text == "=":
            b.configure(command=lambda: sendToServer(e))
        b.grid(row=r, column=c)
        if text in operators + ['√']:
            btns[text] = b
        tk_elements[i] = b
        c += 1
        if c == column_limit:
            c = 0
            r += 1
    return tk_elements


w = Tk()
w.title("RAMCalc")
w.iconphoto(True, PhotoImage(file="img/logo.png"))
w.resizable(False, False)

# ===== IMPOSTAZIONE STILE ===== #
s = src.Style.Style(db, w)

ip_address, server = ip()

m = Menu(w)
w.config(menu=m)
fm = Menu(m, tearoff=0)
om = Menu(m, tearoff=0)
hm = Menu(m, tearoff=0)
m.add_cascade(label="File", menu=fm)
history_image = PhotoImage(master=fm, file="img/history.png")
fm.add_command(label="Cronologia", image=history_image,
               compound="left", command=lambda db=db: cronologia(db))
exit_image = PhotoImage(master=fm, file="img/exit.png")
fm.add_command(label="Esci", image=exit_image,
               compound="left", command=w.destroy)
m.add_cascade(label="Impostazioni", menu=om)
brush_image = PhotoImage(master=om, file="img/settings.png")
om.add_command(label="Apri impostazioni", image=brush_image,
               compound="left", command=lambda: Impostazioni(db, s))
plug_image = PhotoImage(master=om, file="img/plug.png")
om.add_command(label="Connetti ad un server...", image=plug_image,
               compound="left", command=lambda: ip(ip_address))
m.add_cascade(label="Aiuto", menu=hm)
info_image = PhotoImage(master=hm, file="img/info.png")
hm.add_command(label="Informazioni", image=info_image,
               compound="left", command=lambda: tkmb.showinfo(parent=w, title="Informazioni su RAMCalc",
                                                              message="Un semplice calcolatore che interpreta dati passati da un computer "
                                                                      "e li elabora in operazioni matematiche, restituendoli ad un altro "
                                                                      "computer.\nRealizzato da maicol07, RichiMassa1 e alecoma"))

e = Entry(w)
e.grid(row=0, column=0, columnspan=3, sticky="nsew")
e.bind('<Return>', lambda e: sendToServer(e.widget))
e.bind('+', lambda event: writeToEntry("+", pressed=True, disable_others=True))
e.bind('-', lambda event: writeToEntry("-", pressed=True, disable_others=True))
e.bind('*', lambda event: writeToEntry("×", pressed=True, disable_others=True))
e.bind('/', lambda event: writeToEntry("÷", pressed=True, disable_others=True))
e.bind('<BackSpace>', lambda event: writeToEntry("", reenable_others=True))
e.bind('<Delete>', lambda event: writeToEntry("", reenable_others=True))

btns = {}
operators = ["+", "-", "×", "÷"]
nf = Frame(w)
nf.grid(row=1, column=1)
buttons(nf, list(range(1, 10)) + ["√", 0, "="])

of = Frame(w)
of.grid(row=1, column=2, rowspan=2)
buttons(of, operators, column_limit=1)

e.focus_set()
w.mainloop()
db.close()  # Chiusura database
if server is not None:
    server.kill()
