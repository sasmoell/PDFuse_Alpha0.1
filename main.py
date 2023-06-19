import tkinter.messagebox
from tkinter import ttk, filedialog
from functions import *


# Funktionen für das Menü

def ausgabeordner_anlegen():
    if os.path.exists("output/mergeoutput") and os.path.exists("output/splits"):
        gen_message_info("Info", "Die Ordner existieren bereits.")
    else:
        try:
            ordner_pruefen_und_erstellen("output/mergeoutput")
            ordner_pruefen_und_erstellen("output/splits")
        except OSError:
            gen_error("Fehler", "Erstellen war nicht möglich.")


# Funktionen für den Fuser-Bereich
def fuser_durchsuchen_button():
    global eingabe_ordner
    try:
        eingabe_ordner = filedialog.askdirectory()
        if eingabe_ordner:
            print("Ausgewählter Ordner:", eingabe_ordner)  # Dient nur als Ausgabe auf der Konsole zur Kontrolle
            file_label01.config(text=eingabe_ordner)
            return eingabe_ordner
    except FileNotFoundError:
        gen_error("Fehler", "Ein unerwarteter Fehler ist aufgetreten.")


def fusenow_button():
    ausgabe_datei = "output/mergeoutput/new_file.pdf"
    try:
        pdf_zusammenfassen(eingabe_ordner, ausgabe_datei)
    except:
        gen_error("Fehler", "Pfad nicht gefunden. 'Ordner suchen' benutzen um den Pfad anzugeben")


def fuser_ausgabeordner_oeffnen_button():
    ordner_pruefen_und_erstellen("output/mergeoutput")
    if os.path.exists("output/mergeoutput"):
        ordner_oeffnen("output")
    elif not os.path.exists("output/mergeoutput"):
        gen_message_info("Hinweis", "Kein Ordner vorhanden.")


# Funktionen für den Splitter
def splitter_durchsuchen_button():
    global quelldatei
    try:
        quelldatei = filedialog.askopenfilename()
        if quelldatei:
            print("Ausgewählte Datei:", quelldatei)
            file_label02.config(text=quelldatei)
            return quelldatei
    except FileNotFoundError:
        gen_error("Fehler", "Datei nicht gefunden oder nicht lesbar.")


def splitnow_button():
    split_output_ordner = "output/splits"
    try:
        pdf_splitten(quelldatei, split_output_ordner)
    except:
        gen_error("Fehler", "Datei nicht gefunden. 'Datei suchen' benutzen um die Datei zu suchen.")


def splitter_ausgabeordner_oeffnen_button():
    ordner_pruefen_und_erstellen("output/splits")
    if os.path.exists("output/splits"):
        ordner_oeffnen("output")
    elif not os.path.exists("output/splits"):
        gen_message_info("Hinweis", "Kein Ordner vorhanden.")


root = tk.Tk()
root.title("PDF 2Fuse & Split Alpha 0.2.0623")
root.config(pady=20, padx=20)
# root.geometry("400x400")
root.resizable(False, False)

# Menübar mit Funktionen

menubar = tk.Menu(root)
root.config(menu=menubar)


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
hilfemenu.add_command(label="ReadMe")
hilfemenu.add_separator()
hilfemenu.add_command(label="Update")

# Styles
style = ttk.Style()
style.configure('redBTN.TButton', background='red', foreground='red')
style.configure("greenBTN.TButton", backgorund="green", foreground="green")

# Seite 01
seite01 = ttk.Frame(root)
seite01.grid(row=0, pady=(0, 20))

titel01 = ttk.Label(seite01, text="PDF 2Fuse & Split", font=("Arial", 24))
titel01.grid()

desc01_label = ttk.Label(seite01, text="Tool zum Teilen und Aufteilen von PDF-Dokumenten")
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
beenden_button.grid(row=2, sticky=tkinter.E, pady=(15, 0))

root.mainloop()
