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
            file_label.config(text=eingabe_ordner)
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
            splitfile_label.config(text=quelldatei)
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


### --------------------------- GUI mit Tkinter --------------------------- ###

root = tk.Tk()
root.title("PDFuse Alpha 0.1.0523")
root.config(pady=20, padx=20)
root.resizable(False, False)

# MENÜ
menubar = tk.Menu(root)

dateimenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Datei", menu=dateimenu)
dateimenu.add_command(label="PDFuser öffnen")
dateimenu.add_command(label="PDFSplitter öffnen")
dateimenu.add_command(label="Ausgabeordner öffnen", command=lambda: ordner_oeffnen("output"))
dateimenu.add_separator()
dateimenu.add_command(label="Beenden", command=root.destroy)

optionenmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Optionen", menu=optionenmenu)
optionenmenu.add_command(label="Ausgabeordner anlegen", command=ausgabeordner_anlegen)
optionenmenu.add_separator()

hilfemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Hilfe", menu=hilfemenu)
hilfemenu.add_command(label="ReadMe")
hilfemenu.add_command(label="Lizenz")

root.config(menu=menubar)

# Frame-Style - Definiert einen Rahmen um Frames
style = ttk.Style()
style.configure('style.TFrame', borderwidth=2, relief='solid')

############ ---------------- SEITE 01 ---------------- ############
pag01frame = ttk.Frame(root)
pag01frame.grid()
# PDFuser Kopfbereich
headframe = ttk.Frame(pag01frame)
headframe.grid(pady=(0, 15), row=0)

title_label = ttk.Label(headframe, text="PDFuser", font=("Arial", 22))
title_label.grid()

desc_label = ttk.Label(headframe, text="Bitte Ordner auswählen, in dem sich die PDF-Dateien befinden.")
desc_label.grid()

# PDFuser Hauptbereich mit Ordnerauswahl
dir_frame = ttk.Frame(pag01frame, style="style.TFrame", padding=10)
dir_frame.grid(row=1)

input_label = ttk.Label(dir_frame, text="Ordner auswählen:")
input_label.grid(row=1, column=0)

file_label = ttk.Label(dir_frame, width=50, anchor="center")
file_label.config(text="...")
file_label.grid(row=2, column=0)

dir_button = ttk.Button(dir_frame, text="Ordner suchen", command=fuser_durchsuchen_button)
dir_button.grid(row=3, column=0)

# PDFuser Button Sektion
buttonframe1 = ttk.Frame(pag01frame)
buttonframe1.grid(row=2, pady=15)

merge_button = ttk.Button(buttonframe1)
merge_button.grid(row=0, column=0)

merge_button.configure(text="Fuse NOW!", command=fusenow_button)
outdir_button = ttk.Button(buttonframe1, text="Ausgabeordner öffnen", command=fuser_ausgabeordner_oeffnen_button)
outdir_button.grid(row=0, column=1)

############ ---------------- SEITE 02 ---------------- ############

pag02frame = ttk.Frame(root)
pag02frame.grid()

# PDFSplitter Kopfbereich mit Ordnerauswahl
headframe2 = ttk.Frame(pag02frame)
headframe2.grid(pady=(15, 0), row=3)

title_label = ttk.Label(headframe2, text="PDFSplitter", font=("Arial", 22))
title_label.grid()

splitdesc_label = ttk.Label(headframe2, text="Bitte wählen Sie zunächst die Datei aus.")
splitdesc_label.grid()

# PDFSplitter Hauptbereich mit Ordnerauswahl
splitframe = ttk.Frame(pag02frame, style="style.TFrame", padding=10)
splitframe.grid(row=4, pady=(15, 0))

splitinput_label = ttk.Label(splitframe, text="Datei auswählen: ")
splitinput_label.grid(row=0, column=0)

splitfile_label = ttk.Label(splitframe, width=50, anchor="center")
splitfile_label.config(text="...")
splitfile_label.grid(row=1, column=0)

splitdir_button = ttk.Button(splitframe, text="Datei suchen", command=splitter_durchsuchen_button)
splitdir_button.grid(row=2, column=0)

# PDFSplitter Button

buttonframe2 = ttk.Frame(pag02frame)
buttonframe2.grid(pady=15, row=5)

split_button = ttk.Button(buttonframe2)
split_button.grid(row=0, column=0)
split_button.configure(text="Split NOW!", command=splitnow_button)

splitoutdir_button = ttk.Button(buttonframe2, text="Ausgabeordner öffnen", command=splitter_ausgabeordner_oeffnen_button)
splitoutdir_button.grid(row=0, column=1)


############ ---------------- Hauptfenster ---------------- ############

# Beenden-Button unten rechts

style = ttk.Style()
style.configure('redBTN.TButton', background='red', foreground='red')

quit_button = ttk.Button(root, text="Beenden", command=root.destroy, style='redBTN.TButton')
quit_button.grid(row=6, column=0, sticky=tkinter.E, pady=(15, 0))

root.mainloop()
