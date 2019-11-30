from tkinter import *
from tkinter.ttk import *


def cronologia(db):
    w = Toplevel()
    w.title("Cronologia - RAMCalc"),
    w.iconphoto(False, PhotoImage(file="img/logo.png"))
    t = Text(w)
    t.pack()
    r = db.select('cronologia')
    text = ""
    if not r.all():
        text = "La cronologia è vuota! Effettua qualche operazione per poter visualizzare qualcosa qui!"
    else:
        for row in r.all():
            text += "{} = {}\n".format(row.expression, row.result)
    t.insert(END, text)
    t.config(state=DISABLED)
    w.mainloop()
