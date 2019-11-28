import os.path
import platform
import sys
import tkinter.messagebox as tkmb


def import_pil(prefix=''):
    """
    Effettua vari controlli alla versione dell'interprete Python installato nel sistema per verificare la sua
    compatibilità con la versione integrata della libreria Pillow.
    In caso positivo, la libreria viene importata, altrimenti viene specificato un messaggio di errore, specificando il
    problema riscontrato.

    :param prefix: Se la chiamata della funzione avviene da un modulo (cartella 'modules') sarà necessario inserire un
    prefisso per importare correttamente la libreria
    :return:
    """
    py_version = sys.version_info
    if py_version <= (3, 5):  # Verifico che la versione di Python installata sia superiore o uguale a 3.5 per il
        # corretto funzionamento del programma. In caso negativo, lancio un messaggio di errore ed esco
        tkmb.showerror(title="Versione di Python non supportata",
                       message="La versione di Python attualmente installata ({}.{}.{}) non è supportata. Aggiornare "
                               "alla versione 3.5 o successive".format(py_version.major, py_version.minor,
                                                                       py_version.micro))
        exit()

    system = platform.system().lower()
    if system != "linux":  # escludo linux in quanto ha già Pillow installato di default
        if system == "windows":
            if platform.architecture()[0] == "32bit":
                os_info = "win32"
            else:
                os_info = "win-amd64"
        else:
            if py_version <= (3, 7):  # Se la versione di Python installata è minore della 3.7 su MAC il programma non
                # funzionerà correttamente. Lancio un messaggio di errore ed esco.
                tkmb.showerror(title="Versione di Python non supportata",
                               message="È stato rilevato che il sistema in uso è MAC OS X. La versione di Python "
                                       "attualmente installata ({}.{}.{}) non è supportata su questo tipo di sistema. "
                                       "Aggiornare alla versione 3.7 o successive".format(py_version.major,
                                                                                          py_version.minor,
                                                                                          py_version.micro))
                exit()
            os_info = "macosx-10.14-x86_64"
        sys.path.insert(0, os.path.abspath("{}lib/PIL/Pillow-6.1.0-py{}.{}-{}.egg".format(prefix, py_version.major,
                                                                                          py_version.minor, os_info)))
