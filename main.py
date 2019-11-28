import sys
import os

sys.path.insert(0, 'lib')
# ========== CLASSI ========== #
from src.common import import_pil

import_pil()

from tkinter import *
from tkinter.ttk import *
import tkinter.simpledialog
from lib.medoo import Medoo
import src.Style
from modules.settings import *

# Apertura database (viene creato se non esiste già il file) e creazione tabelle se non esistono già
if not (os.path.exists(os.path.expanduser('~/Documents/RAMCalc'))):
    os.makedirs(os.path.expanduser('~/Documents/RAMCalc'))
    open(os.path.expanduser('~/Documents/RAMCalc/db.db'), "w").close()  # Creazione file database
db = Medoo('sqlite', database=os.path.expanduser('~/Documents/RAMCalc/db.db'))
query = open("tables.sql")
db.connection.executescript(query.read())
query.close()


def writeToEntry(text):
    e.insert("end", text)

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
        b = Button(frame, text=text, command=lambda: writeToEntry(text))
        b.grid(row=r, column=c)
        tk_elements[i] = b
        c += 1
        if c == column_limit:
            c = 0
            r += 1
    return tk_elements


w = Tk()
w.title("RAMCalc")
w.iconphoto(True, PhotoImage(file="img/logo.png"))

ip = tkinter.simpledialog.askstring("Indirizzo IP",
                                    "Digita l'indirizzo IP del server. Se il server è sul tuo computer digita "
                                    "localhost o 127.0.0.1.\nSe premi Annulla o non immetti nulla verrà avviato il "
                                    "server interno.",
                                    parent=w)
if ip is None:
    import subprocess

    process = subprocess.Popen("server.py", shell=True, stdout=subprocess.PIPE)
    ip = "localhost"
# ===== IMPOSTAZIONE STILE ===== #
s = src.Style.Style(db, w)

m = Menu(w)
w.config(menu=m)
fm = Menu(m, tearoff=0)
om = Menu(m, tearoff=0)
hm = Menu(m, tearoff=0)
m.add_cascade(label="File", menu=fm)
exit_image = PhotoImage(master=fm, file="img/exit.png")
fm.add_command(label="Esci", image=exit_image,
               compound="left", command=w.destroy)
m.add_cascade(label="Impostazioni", menu=om)
brush_image = PhotoImage(master=om, file="img/settings.png")
om.add_command(label="Apri impostazioni", image=brush_image,
               compound="left", command=lambda: Impostazioni(db, s))
m.add_cascade(label="Aiuto", menu=hm)
info_image = PhotoImage(master=hm, file="img/info.png")
hm.add_command(label="Informazioni", image=info_image,
               compound="left", command=lambda: tkmb.showinfo(parent=w, title="Informazioni su RAMCalc",
                                                              message="Un semplice calcolatore che interpreta dati passati da un computer "
                                                                      "e li elabora in operazioni matematiche, restituendoli ad un altro "
                                                                      "computer.\nRealizzato da maicol07, RichiMassa1 e alecoma"))

e = Text(w, height=1)
e.grid(row=0, column=0, columnspan=3)

mf = Frame(w)
mf.grid(row=1, column=0, rowspan=2)
math_functions = ["sin", "cos", "tan", "sqrt", "log", "loga(b)", "ln", "x²", "x³", "x^n", "|x|", "("]
buttons(mf, math_functions)

nf = Frame(w)
nf.grid(row=1, column=1)
buttons(nf, list(range(1, 10)) + [")", 0, "="])

operators = ["+", "-", "×", "÷"]
of = Frame(w)
of.grid(row=1, column=2, rowspan=2)
buttons(of, operators, column_limit=1)

w.mainloop()
db.close()  # Chiusura database
