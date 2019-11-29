from tkinter import Tk

from lib.medoo.database.sqlite import Sqlite
from lib.ttkthemes.themed_style import ThemedStyle

s = None


class Style:
    __windows = []

    def __init__(self, db, root):
        """
        Inizializzazione dello stile Tkinter personalizzato (libreria ttkthemes)

        :param Sqlite db:
        :param Tk root: Finestra root creata con Tk() e non con Toplevel()
        """
        global s
        s = self

        self.__db = db
        self.style = ThemedStyle()
        s = self.style
        self.bgcolor = self.style.lookup("TButton", "background", default="white")
        self.change_window_bg(root)
        try:
            font = self.__db.get("impostazioni", "value", where={"setting": 'font'})
            if font:
                self.current_font = font
                self.style.configure('.', font=self.current_font)
        except TypeError:
            pass
        try:
            theme = self.__db.get("impostazioni", "value", where={"setting": "theme"})
            if theme:
                self.current_theme = theme
                self.update_style(theme)
        except TypeError:
            pass

    def update_style(self, theme):
        """
        Cambia tema

        :param theme:
        :return:
        """
        self.style.set_theme(theme)
        self.bgcolor = self.style.lookup("TButton", "background", default="white")
        if self.bgcolor == "SystemButtonFace":
            self.bgcolor = "white"
        self.style.configure("TFrame", background=self.bgcolor)
        self.style.configure("TButton", height=100)
        self.style.configure("TLabel", background=self.bgcolor)
        self.style.configure("TPhotoimage", background=self.bgcolor)
        self.style.configure("TLabelframe", background=self.bgcolor)
        self.style.configure("TLabelframe.Label", background=self.bgcolor)
        self.style.configure("TScale", background=self.bgcolor)
        self.style.configure("TCheckbutton", background=self.bgcolor)
        for i in self.__windows:
            self.change_window_bg(i)

    def change_window_bg(self, w):
        """
        Modifica lo sfondo della finestra passata come parametro e la aggiunge alla lista di quelle già aperte, se non
        è già stata inserita

        :param w:
        :return:
        """
        w.configure(background=self.bgcolor)
        if not (w in self.__windows):
            self.__windows.append(w)

    def close_window(self, w):
        """
        Rimuove dalla lista delle finestre al momento aperte l'oggetto della finestra passata come parametro

        :param w:
        :return:
        """
        self.__windows.remove(w)

    def set_theme(self, theme):
        """
        Salva il tema nel database e lo cambia utilizzando il metodo update_style

        :param theme:
        :return:
        """
        if hasattr(self, "current_theme"):
            self.__db.update("impostazioni", {"value": theme}, where={"setting": "theme"})
        else:
            self.__db.insert("impostazioni", "setting, value", ("theme", theme))
        self.update_style(theme)
        self.current_theme = theme

    def set_font(self, font):
        if hasattr(self, "current_font"):
            self.__db.update("impostazioni", {"value": font}, where={"setting": "font"})
        else:
            self.__db.insert("impostazioni", "setting, value", ("font", font))
        self.current_font = font
        self.style.configure('.', font=self.current_font)

    def get_themes_list(self):
        """
        Ritorna la lista dei temi disponibili
        :return:
        """
        return self.style.theme_names()

    def get_current_theme_name(self):
        """
        Ritorna il nome del tema attualmente impostato
        :return:
        """
        return self.style.theme_use()

    def get_current_font(self):
        """
        Ritorna il nome del carattere attualmente impostato. Se si sta usando quello predefinito verrà restituito
        "default"

        :return:
        """
        if hasattr(self, "current_font"):
            return self.current_font
        else:
            return 'default'


def change_window_bg(w):
    """
    Modifica lo sfondo della finestra passata come parametro e la aggiunge alla lista di quelle già aperte, se non
    è già stata inserita

    :param w:
    :return:
    """
    bgcolor = s.lookup("TButton", "background", default="white")
    if bgcolor == "SystemButtonFace":
        bgcolor = "white"
    w.configure(background=bgcolor)
