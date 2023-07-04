import os
import tkinter as tk
from tkinter import ttk, filedialog
import functions as fu


# # # # # # Funktionen für die Menüleiste # # # # # #

# datei_seitenwahl() ermöglicht die Navigation durch die GUI über die Menüleiste. Die ttkFrames werden entsprechend ein- und ausgeblendet.
def datei_seitenwahl(seite):
    seite01.grid()
    seite02.grid_remove()
    seite03.grid_remove()

    if seite == 1:
        seite01.grid(row=0)
    elif seite == 2:
        seite02.grid(row=1)
    elif seite == 3:
        seite03.grid(row=1)


# Die Funktion ausgabeordner() anlegen überprüft, ob die Standard-Ausgabeordner vorhanden sind. Falls nicht wird mit der Funktion ordner_pruefen_und_erstellen() aus dem Modul functions.py die Ordner angelegt.
def ausgabeordner_anlegen():
    if os.path.exists("output/mergeoutput") and fu.os.path.exists("output/splits"):
        fu.gen_message_info("Info", "Die Ordner existieren bereits.")
    else:
        try:
            fu.ordner_pruefen_und_erstellen("output/mergeoutput")
            fu.ordner_pruefen_und_erstellen("output/splits")
        except OSError:
            fu.gen_error("Fehler", "Erstellen war nicht möglich.")


# Die Funktion menu_doku() ist in der Menüleiste -> Hilfe -> Dokumentation gebunden. Sie ruft aus einem mitgelieferten Unterordner eine index.html mit der Dokumentation zum Programm auf.
def menu_doku():
    try:
        fu.hilfe_aufrufen("fuser\index.html")
    except FileNotFoundError:
        try:
            fu.hilfe_aufrufen("fuser/index.html")
        except FileNotFoundError:
            fu.gen_error("Fehler", "Die Hilfe konnte nicht geöffnet werden.")


# Funktion für Menüleiste -> Hilfe -> Update-Check
# Für die Funktion wird eine aktive Verbindung ins Internet benötigt. Es wird erst versucht die aktuelle Versionsnummer abzurufen. Anschließend wird versucht die aktuelle Versionsnummer mit der abgerufenen Nummer zu vergleichen

def update_menu_button():
    try:
        fu.versionsnummer_online_pruefen()
    except:
        fu.gen_error("Prüfung fehlgeschlagen",
                            "Die Überprüfung ist fehlgeschlagen. Stellen Sie sicher, dass Sie mit dem Internet verbunden sind.")
    try:
        fu.update_check()
    except:
        fu.gen_error("Fehler", "Versionsnummer konnte nicht ermittelt werden.")


# # # # # # Funktionen für den Fuser PDF-Dateien zusammenfügen # # # # # #

# Die Funktion fuser_durchsuchen_button() setzt zunächst eingabe_ordner als globale Variabel:
# TODO: https://github.com/sasmoell/PDFuse_Alpha0.1/issues/6#issue-1778433299 (Globale Variable vermeiden)
# Öffnet ein File-Dialog und speichert den ausgewählten Ordner als String. Zudem wird das Label aktualisiert, um den gewählten Ordner auf der GUI auszugeben. Die print-Anweisung dient nur für den Entwickler zum debuggen.
def fuser_durchsuchen_button():
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
    ausgabe_datei = "output/mergeoutput/new_file.pdf"
    try:
        fu.pdf_zusammenfassen(eingabe_ordner, ausgabe_datei)
    except:
        fu.gen_error("Fehler", "Pfad nicht gefunden. 'Ordner suchen' benutzen um den Pfad anzugeben")


# Die Funktion fuser_ausgabeordner_oeffnen_button() ruft zunächst aus fuctions.py die Funktion ordner_pruefen_und_erstellen() auf, um zu prüfen, ob die Standardordner vorhanden sind. Wenn die Standardordner vorhanden sind, wird der Pfad geöffnet. Der Benutzer muss so nicht lange in seinem Dateisystem suchen und kommt direkt zum Zielordner.
# TODO: https://github.com/sasmoell/PDFuse_Alpha0.1/issues/3#issue-1774093733
def fuser_ausgabeordner_oeffnen_button():
    fu.ordner_pruefen_und_erstellen("output/mergeoutput")
    if fu.os.path.exists("output/mergeoutput"):
        fu.ordner_oeffnen("output")
    elif not fu.os.path.exists("output/mergeoutput"):
        fu.gen_message_info("Hinweis", "Kein Ordner vorhanden.")


# Funktionen für den Splitter

# Globale Variabel 'quelldatei' wird gesetzt.
# TODO: https://github.com/sasmoell/PDFuse_Alpha0.1/issues/6#issue-1778433299 (Globale Variable vermeiden)

# Öffnet ein File-Dialog und speichert den ausgewählten Ordner als String. Zudem wird das Label aktualisiert, um den gewählten Ordner auf der GUI auszugeben. Die print-Anweisung dient nur für den Entwickler zum debuggen.
def splitter_durchsuchen_button():
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
    split_output_ordner = "output/splits"
    try:
        fu.pdf_splitten(quelldatei, split_output_ordner)
    except:
        fu.gen_error("Fehler", "Datei nicht gefunden. 'Datei suchen' benutzen um die Datei zu suchen.")


# Die Funktion splitter_ausgabeordner_oeffnen_button() ruft zunächst aus fuctions.py die Funktion ordner_pruefen_und_erstellen() auf, um zu prüfen, ob die Standardordner vorhanden sind. Wenn die Standardordner vorhanden sind, wird der Pfad geöffnet. Der Benutzer muss so nicht lange in seinem Dateisystem suchen und kommt direkt zum Zielordner.
def splitter_ausgabeordner_oeffnen_button():
    fu.ordner_pruefen_und_erstellen("output/splits")
    if fu.os.path.exists("output/splits"):
        fu.ordner_oeffnen("output")
    elif not fu.os.path.exists("output/splits"):
        fu.gen_message_info("Hinweis", "Kein Ordner vorhanden.")


# # # # # # Tkinter Benutzeroberfläche # # # # # #

if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"PDF 2Fuse & Split Alpha {fu.current_version}")
    root.config(pady=20, padx=20)
    # root.geometry("400x400")
    root.resizable(False, False)

    # Menübar mit Funktionen

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    dateimenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datei", menu=dateimenu)
    dateimenu.add_command(label="PDF zusammenfügen (Fuser)", command=lambda: datei_seitenwahl(2))
    dateimenu.add_command(label="PDF teilen (Splitter)", command=lambda: datei_seitenwahl(3))
    dateimenu.add_separator()
    dateimenu.add_command(label="Beenden", command=root.destroy)

    optionenmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Optionen", menu=optionenmenu)
    optionenmenu.add_command(label="Ordner anlegen", command=ausgabeordner_anlegen)

    hilfemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Hilfe", menu=hilfemenu)
    hilfemenu.add_command(label="Info")
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

    ausgabedir_button = ttk.Button(seite02_btn, text="Ausgabeordner öffnen", command=fuser_ausgabeordner_oeffnen_button)
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

    ausgabedir_button = ttk.Button(seite03_btn, text="Ausgabeordner öffnen", command=fuser_ausgabeordner_oeffnen_button)
    ausgabedir_button.grid(row=0, column=1)
    ausgabedir_button.configure(padding=(5, 10))

    # B E E N D E N ########

    beenden_button = ttk.Button(root, text="Beenden", command=root.destroy, style='redBTN.TButton')
    beenden_button.grid(row=2, sticky=tk.E, pady=(15, 0))

    root.mainloop()
