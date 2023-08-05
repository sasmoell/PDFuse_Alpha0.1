######################################################################################
### Author: Sascha Möller, 2023 ######################################################
### Contact: sasmoell@t-online.de #### With great power comes great responsibility ###
### PDFuse Alpha 0.1 #################################################################
######################################################################################

import os
import subprocess
from tkinter import ttk, filedialog
import tkinter as tk
import functions as fu

##############################################################################################################
#####-Funktionen für die Menüleiste-##########################################################################
##############################################################################################################

# Ermöglicht die Navigation über die Menüleiste. TtkFrames werden entsprechend ein- und ausgeblendet.
def menu_navigation(seite):
    """
    Hier wird der Grid-Layout-Manager verwendet, um Tkinter-Inhalte ein- bzw. auszublenden. Zu Beginn ist
    Seite 1 eingeblendet. Wenn eine andere Auswahl getroffen wird, werden alle anderen Inhalte mit grid_remove()
    ausgeblendet.
    :param seite:
    :return:
    """
    seite01.grid()
    seite02.grid_remove()
    seite03.grid_remove()
    seite_info.grid_remove()

    if seite == 1:
        seite01.grid(row=0)
    elif seite == 2:
        seite02.grid(row=1)
    elif seite == 3:
        seite03.grid(row=1)
    elif seite == 4:
        seite_info.grid(row=1)


# Menüleiste -> Hilfe -> Dokumentation. Ruft eine lokale index.html auf.
def menu_doku():
    """
    Im Projektordner ist der Ordner 'fuser' enthalten. Darin befindet sich die Dokumentation für die Benutzer des
    Programms. Die Dokumentation wurde mit HTML und CSS erstellt. Diese Funktion ruft die index.html auf und versucht
    sie mit dem Standard-Programm (i.d.R. der Standard-Browser des Systems) für HTML zu öffnen.
    :return:
    """
    try:
        os.startfile("fuser\\index.html")
    except FileNotFoundError:
        try:
            os.startfile("fuser/index.html")
        except FileNotFoundError:
            try:
                dateipfad = "fuser/index.html"
                subprocess.run(["xdg-open", dateipfad])
            except FileNotFoundError:
                fu.gen_error("Fehler", "Die Hilfe konnte nicht geöffnet werden.")


# Menüleiste -> Hilfe -> Update-Check
# Verbindung ins Internet wird benötigt. Aktuelle Versionsnummer abrufen und vergleichen.

def update_menu_button():
    """
    Diese Funktion überprüft, ob ein Update für das Programm online verfügbar ist. Dazu bedient es sich u.a. der
    Funktionen onlineversion_pruefen() und update_check() aus dem functions-Modul.
    :return:
    """
    try:
        fu.onlineversion_pruefen()
    except ConnectionError:
        fu.gen_error("Prüfung fehlgeschlagen",
                     "Die Überprüfung ist fehlgeschlagen. Stellen Sie sicher, dass Sie mit dem Internet verbunden sind.")
    try:
        fu.update_check()
    except FileNotFoundError:
        fu.gen_error("Fehler", "Versionsnummer konnte nicht ermittelt werden.")


##############################################################################################################
#####-Funktionen für PDF zusammenfügen (Fuser)-###############################################################
##############################################################################################################

# Öffnet ein File-Dialog und speichert den ausgewählten Ordner als String.
# TODO: https://github.com/sasmoell/PDFuse_Alpha0.1/issues/6#issue-1778433299 (Globale Variable vermeiden)

def fuser_durchsuchen_button():
    """
    Die Funktion fuser_durchsuchen_button() ist dafür zuständig den Ordner auszuwählen, in dem sich die PDF-Dokumente
    befinden. Der Ordnerpfad wird als Variable benötigt. Dazu setzt die Funktion zunächst eingabe_ordner als globale
    Variabel. Anschließend wird versucht per filedialog nach dem Ordner gefragt und der Label-Text aktualisiert.
    Sollte es zu einer Ausnahme kommen, wird ein FileNotFoundError ausgegeben. Die globale Variabel und deren Vermeidung
    ist ein Thema auf GitHub https://github.com/sasmoell/PDFuse_Alpha0.1/issues/6#issue-1778433299
    :return:
    """
    global eingabe_ordner
    try:
        eingabe_ordner = filedialog.askdirectory()
        if eingabe_ordner:
            print("Ausgewählter Ordner:", eingabe_ordner)  # nur für debugging benötigt
            file_label01.config(text=eingabe_ordner)
    except FileNotFoundError:
        fu.gen_error("Fehler", "Ein unerwarteter Fehler ist aufgetreten.")


# Die Funktion fusenow_button() erstellt den Pfad/Name der Ausgabedatei und versucht aus der functions.py die Funktion pdf_zusammenfassen() aufzurufen
# Merger TODO: https://github.com/sasmoell/PDFuse_Alpha0.1/issues/4#issue-1774099062

def fusenow_button():
    """
    Die Funktion ist mit dem Button FuseNOW verbunden. Es wird versucht die Funktion pdf_zusammenfassen aus dem Modul
    functions.py aufzurufen. Damit das möglich ist, muss zuvor die Variabel ausgabe_datei initialisiert werden. Sollte
    es zu einer Ausnahme kommen, wird ein FileNotFoundError ausgelöst.
    :return:
    """
    ausgabe_datei = "output/mergeoutput/new_file.pdf"
    try:
        fu.pdf_zusammenfassen(eingabe_ordner, ausgabe_datei)
    except FileNotFoundError as e:
        fu.gen_error("Fehler", f"Pfad nicht gefunden. 'Ordner suchen' benutzen um den Pfad anzugeben. Fehler: {e}")
    except NameError as e:
        fu.gen_error("Fehler", f"Es wurde kein Pfad gefunden. Fehler: {e}")


##############################################################################################################
#####-Funktionen für PDF teilen (Splitter)-###################################################################
##############################################################################################################

# Globale Variabel 'quelldatei' wird gesetzt.
# TODO: https://github.com/sasmoell/PDFuse_Alpha0.1/issues/6#issue-1778433299 (Globale Variable vermeiden)
# Öffnet ein File-Dialog und speichert den ausgewählten Ordner als String. Zudem wird das Label aktualisiert, um den gewählten Ordner auf der GUI auszugeben. Die print-Anweisung dient nur für den Entwickler zum debuggen.

def splitter_durchsuchen_button():
    """
    Die Funktion splitter_durchsuchen_button() ist dafür zuständig, die Datei auszuwählen, in dem sich das PDF-Dokument
    befindet. Der Dateipfad wird als Variable benötigt. Dazu setzt die Funktion zunächst quelldatei als globale
    Variabel. Anschließend wird versucht per filedialog nach der Datei gefragt und der Label-Text aktualisiert. Sollte
    es zu einer Ausnahme kommen, wird ein FileNotFoundError ausgegeben. Die globale Variabel und deren Vermeidung ist
    ein Thema auf GitHub https://github.com/sasmoell/PDFuse_Alpha0.1/issues/6#issue-1778433299
    :return:
    """
    global quelldatei
    try:
        quelldatei = filedialog.askopenfilename()
        if quelldatei:
            print("Ausgewählte Datei:", quelldatei)
            file_label02.config(text=quelldatei)
            return quelldatei
    except FileNotFoundError:
        fu.gen_error("Fehler", "Datei nicht gefunden oder nicht lesbar.")


# Die Funktion splitnow_button() erstellt eine Variabel mit einem Standard-Ordnerpfad und versucht aus der functions.py die Funktion pdf_splitten() aufzurufen
def splitnow_button():
    """
    Der Standard-Ordner für die erzeugten Dateien wird gesetzt unter output/splits. Die Ordnerstruktur wird unter dem
    Hauptverzeichnis des Programms erzeugt. Aus dem functions-Modul wird die Funktion pdf_splitten aufgerufen um die
    einzelnen Seiten aus der Datei zu extrahieren.
    :return:
    """
    split_output_ordner = "output/splits"
    try:
        fu.pdf_splitten(quelldatei, split_output_ordner)
    except FileNotFoundError as e:
        fu.gen_error("Datei nicht gefunden", f"Hups! Die Datei wurde nicht gefunden. Wurde sie zwischenzeitlich verschoben? Bitte nutzen Sie den Button 'Datei suchen' um die Datei anzugeben.\n\nFehlermeldung: {e}")
    except NameError as e:
        fu.gen_error("Datei nicht gefunden", f"Bitte nutzen Sie den Button 'Datei suchen' um die Datei anzugeben.\n\nFehlermeldung: {e}")


##############################################################################################################
######-Tkinter Benutzeroberfläche (GUI)-######################################################################
##############################################################################################################

if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"PDF 2Fuse & Split Alpha {fu.current_version}")
    root.config(pady=20, padx=20)
    root.iconbitmap("fuser_icon.ico")
    root.resizable(False, False)

    # Menübar mit Funktionen

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    dateimenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datei", menu=dateimenu)
    dateimenu.add_command(label="PDF zusammenfügen (Fuser)", command=lambda: menu_navigation(2)) # Die Verwendung von lambda ermöglicht die Verwendung des Parameters
    dateimenu.add_command(label="PDF teilen (Splitter)", command=lambda: menu_navigation(3))
    dateimenu.add_separator()
    dateimenu.add_command(label="Beenden", command=root.destroy)

    optionenmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Optionen", menu=optionenmenu)
    optionenmenu.add_command(label="Ordner anlegen", command=lambda: fu.ausgabeordner_anlegen())

    hilfemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Hilfe", menu=hilfemenu)
    hilfemenu.add_command(label="Info", command=lambda: menu_navigation(4))
    hilfemenu.add_command(label="Dokumentation", command=menu_doku)
    hilfemenu.add_separator()
    hilfemenu.add_command(label="Update-Check", command=update_menu_button)
    hilfemenu.add_command(label="Update Download", command=lambda: fu.update_seite_oeffnen())

    # Styles
    style = ttk.Style()
    style.configure('redBTN.TButton', background='red', foreground='red')
    style.configure("greenBTN.TButton", backgorund="green", foreground="green")

    # Seite 01
    seite01 = ttk.Frame(root)
    seite01.grid(row=0, pady=(0, 20))

    titel01 = ttk.Label(seite01, text="PDF 2Fuse & Split", font=("Arial", 24))
    titel01.grid()

    desc01_label = ttk.Label(seite01, text="Tool zum Zusammenfügen und Aufteilen von PDF-Dokumenten")
    desc01_label.grid()

    # Icon
    icon = tk.PhotoImage(file="icon.gif")
    img_label = ttk.Label(seite01, image=icon)
    img_label.place(width=80, relheight=1)
    img_label.grid()

    # Seite 02
    seite02 = ttk.Frame(root)
    seite02.grid(row=1)

    titel02 = ttk.Label(seite02, text="Dateien zusammenfügen", font=("Arial", 16))
    titel02.grid(row=0)

    desc02_label = ttk.Label(seite02, text="Bitte Ordner auswählen, in dem sich die PDF-Dateien befinden.")
    desc02_label.grid(row=1)

    input_label01 = ttk.Label(seite02, text="Ordner auswählen:")
    input_label01.grid(row=2, column=0)

    file_label01 = ttk.Label(seite02, width=50)
    file_label01.config(text="...", anchor="center", foreground="green", font=("Arial", 12), padding=10)
    file_label01.grid(row=3)

    ordner_suchen_button = ttk.Button(seite02, text="Ordner suchen", command=fuser_durchsuchen_button)
    ordner_suchen_button.grid(row=4, pady=(0, 20))

    seite02_btn = ttk.Frame(seite02)
    seite02_btn.grid()

    fuse_button = ttk.Button(seite02_btn)
    fuse_button.grid(row=0, column=0)
    fuse_button.configure(text="Fuse NOW!", command=fusenow_button, padding=(5, 10), style='greenBTN.TButton')

    ausgabedir_button = ttk.Button(seite02_btn, text="Ausgabeordner öffnen",
                                   command=fu.fuser_ausgabeordner_oeffnen_button)
    ausgabedir_button.grid(row=0, column=1)
    ausgabedir_button.configure(padding=(5, 10))

    # Seite 03
    seite03 = ttk.Frame(root)
    seite03.grid_remove()

    titel03 = ttk.Label(seite03, text="Datei splitten", font=("Arial", 16))
    titel03.grid(row=0)

    desc03_label = ttk.Label(seite03, text="Bitte Datei auswählen, um sie zu splitten.")
    desc03_label.grid(row=1)

    input_label02 = ttk.Label(seite03, text="Datei auswählen:")
    input_label02.grid(row=2, column=0)

    file_label02 = ttk.Label(seite03, width=50)
    file_label02.config(text="...", anchor="center", foreground="green", font=("Arial", 12), padding=10)
    file_label02.grid(row=3)

    datei_suchen_button = ttk.Button(seite03, text="Datei suchen", command=splitter_durchsuchen_button)
    datei_suchen_button.grid(row=4, pady=(0, 20))

    seite03_btn = ttk.Frame(seite03)
    seite03_btn.grid()

    split_button = ttk.Button(seite03_btn)
    split_button.grid(row=0, column=0)
    split_button.configure(text="Splitt NOW!", command=splitnow_button, padding=(5, 10), style='greenBTN.TButton')

    ausgabedir_button = ttk.Button(seite03_btn, text="Ausgabeordner öffnen",
                                   command=fu.splitter_ausgabeordner_oeffnen_button)
    ausgabedir_button.grid(row=0, column=1)
    ausgabedir_button.configure(padding=(5, 10))

    # Seite Info

    seite_info = ttk.Frame(root)
    seite_info.grid_remove()

    titel_info = ttk.Label(seite_info, text="Über PDFuser Alpha", font=("Arial", 16), padding=10)
    titel_info.grid(row=0)

    text_info01 = ttk.Label(seite_info, text=f"Version: {fu.current_version}", width=78, anchor="center")
    text_info01.grid(row=1)

    text_info01 = ttk.Label(seite_info, text="Author: Sascha Möller")
    text_info01.grid(row=2)

    text_info01 = ttk.Label(seite_info, text="Kontakt: sasmoell@t-online.de")
    text_info01.grid(row=3)

    text_info02 = ttk.Label(seite_info,
                            text="Kommentar: Dieses Programm ist nicht für den produktiven Einsatz\ngedacht. Es ist ein Projekt im Rahmen einer Weiterbildung\nSoftware Developer IHK.",
                            padding=10)
    text_info02.grid(row=4)

    # B E E N D E N #

    beenden_button = ttk.Button(root, text="Beenden", command=root.destroy, style='redBTN.TButton')
    beenden_button.grid(row=2, sticky=tk.E, pady=(15, 0))

    root.mainloop()
