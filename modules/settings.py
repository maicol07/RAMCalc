# ========== LIBRERIE INTERNE ========== #
import tkinter.messagebox as tkmb
from tkinter import *
from tkinter.ttk import *

sys.path.insert(0, 'lib/tkfontchooser-2.0.2-py3.6.egg')
from tkfontchooser import askfont

# ========== CLASSI ========== #
import src.Style


class Impostazioni:
    def __init__(self, db, style):
        """
        Inizializza l'oggetto Impostazioni

        :param db:
        :param src.Style.Style style:
        """
        self.__db = db
        self.__style = style
        w = Toplevel()
        w.title("Impostazioni")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__root = w
        self.__style.change_window_bg(w)

        # ===== CAMBIO TEMA ===== #
        ft = Labelframe(w, text="Cambia tema")
        ft.grid(row=0, column=0, padx=10, pady=10)
        menut = Combobox(ft, postcommand=lambda: menut.configure(values=sorted(self.__style.get_themes_list())))
        menut.set(self.__style.get_current_theme_name())
        menut.grid(row=0, column=0, padx=10, pady=5)
        isave = PhotoImage(file="img/save.png")
        bts = Button(ft, text="SALVA", image=isave, compound=LEFT, command=lambda: self.__style.set_theme(menut.get()))
        bts.grid(row=0, column=1, padx=10, pady=5)

        # ===== CAMBIO CARATTERE ===== #
        ff = Labelframe(w, text="Cambia carattere")
        ff.grid(row=0, column=2, pady=10, padx=10)
        fc = Frame(ff)
        fc.grid(row=0, column=0, pady=5)
        af = Label(fc, text="Carattere attuale:\n {}".format(self.__style.get_current_font().replace("\\", '')))
        af.pack()
        sf = Button(fc, text="Cambia carattere", command=lambda: self.fontcallback(af, btcs))
        sf.pack()
        btcs = Button(ff, text="SALVA", image=isave, compound=LEFT)
        btcs.grid(row=0, column=1, padx=10)

        # ===== IMPORT DATI DI ESEMPIO ===== #
        fde = Labelframe(w, text="Importa dati di esempio")
        fde.grid(row=1, column=1, padx=10, pady=10)
        idown = PhotoImage(file="img/download.png")
        bti = Button(fde, text="Importa", image=idown, compound=LEFT, command=self.import_dati_esempio)
        bti.pack(padx=5, pady=5)
        w.mainloop()

    def fontcallback(self, font_sel, btn):
        """
            Font picker. Seleziona il carattere da utilizzare all'interno dell'applicazione.

            Parametri
            ----------
            :param Label font_sel :
                Etichetta font selezionato.
            :param Button btn :
                Pulsante SALVA

            Ritorna
            -------
            Niente
            """
        # chiedi il font all'utente
        font = askfont(self.__root, title="Selettore carattere")
        # la variabile font è "" se l'utente ha annullato
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            font_sel.configure(font=font_str,
                               text="Carattere selezionato:\n {}".format(font_str.replace('\\', ' ')))
            btn.configure(command=lambda: self.__style.set_font(font_str))

    def import_dati_esempio(self):
        if list(self.__db.select("marche")):
            result = tkmb.askyesno(parent=self.__root, title="Dati già presenti!",
                                   message="Attenzione! Sono già presenti dei dati inseriti. Si vuole veramente "
                                           "sostituirli con i dati di esempio? TUTTI I DATI GIÀ PRESENTI VERRANNO "
                                           "ELIMINATI!")
            if not result:
                return
        self.__db.delete("marche", where=None)
        self.__db.delete("veicoli", where=None)
        data = open("exampledata.sql")
        self.__db.cursor.executescript(data.read())
        data.close()
        tkmb.showinfo(parent=self.__root, title="Dati importati correttamente",
                      message="I dati sono stati importati con successo! Chiudi eventuali finestre aperte relative"
                              "alle marche e ai veicoli.")
