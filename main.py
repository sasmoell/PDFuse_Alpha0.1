import tkinter
from tkinter import ttk
from functions import *

def eingabeordner_button():
    global eingabe_ordner
    try:
        eingabe_ordner = filedialog.askdirectory()
        if eingabe_ordner:
            print("Ausgewählter Ordner:", eingabe_ordner) # Dient nur als Ausgabe auf der Konsole zur Kontrolle
            #file_label.config(text="...")
            file_label.config(text=eingabe_ordner)
            return eingabe_ordner
    except:
        tk.messagebox.showerror(title="Fehler", message="Pfad konnte nicht gesetzt werden.")

def zusammenfassen_button():
    ausgabe_datei = "output/output.pdf"
    try:
        pdf_zusammenfassen(eingabe_ordner, ausgabe_datei)
    except:
        tk.messagebox.showerror(title="Fehler", message="Etwas ist schief gelaufen. Wahrscheinlich konnte der Pfad nicht gefunden werden. Wählen Sie über den Durchsuchen-Button den Ordner aus, in dem sich die PDF-Dateien befinden.")

# GUI mit Tkinter

root = tk.Tk()
root.title("PDFuse Alpha 0.1.0523")
root.config(pady=20, padx=20)
root.resizable(False, False)

#MENÜ
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Datei", menu=filemenu)

filemenu.add_command(label="Merge_Test", command=zusammenfassen_button)
filemenu.add_separator()
filemenu.add_command(label="Ordner öffnen")
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=root.destroy)

root.config(menu=menubar)

# Frame-Style
style = ttk.Style()
style.configure('style.TFrame', borderwidth=2, relief='solid')

#PDFuser Kopfbereich
headframe = ttk.Frame(root)
headframe.grid(pady=(0, 15), row=0)

title_label = ttk.Label(headframe, text="PDFuser", font=("Arial", 22))
title_label.grid()

desc_label = ttk.Label(headframe, text="Bitte Ordner auswählen, in dem sich die PDF-Dateien befinden.")
desc_label.grid()

# Ordnerauswahl Input Bereich
dir_frame = ttk.Frame(root, style="style.TFrame", padding=10)
dir_frame.grid(row=1)

input_label = ttk.Label(dir_frame, text="Ordner auswählen:")
input_label.grid(row=1, column=0)

file_label = ttk.Label(dir_frame, width=50, anchor="center")
file_label.config(text="...")
file_label.grid(row=2, column=0)

dir_button = ttk.Button(dir_frame, text="Durchsuchen", command=eingabeordner_button)
dir_button.grid(row=3, column=0)

# Button Section (PDFuser)
buttonframe1 = ttk.Frame(root)
buttonframe1.grid(row=2, pady=15)

merge_button = ttk.Button(buttonframe1)
merge_button.grid(row=0, column=0)

merge_button.configure(text="Fuse NOW!", command=zusammenfassen_button)
outdir_button = ttk.Button(buttonframe1, text="Ausgabeordner öffnen")
outdir_button.grid(row=0, column=1)


#PDFSplitter Kopfbereich
headframe2 = ttk.Frame(root)
headframe2.grid(pady=(15, 0), row=3)

title_label = ttk.Label(headframe2, text="PDFSplitter", font=("Arial", 22))
title_label.grid()

splitdesc_label = ttk.Label(headframe2, text="Bitte wählen Sie zunächst die Datei aus.")
splitdesc_label.grid()


# SPLIT BEREICH
splitframe = ttk.Frame(root, style="style.TFrame", padding=10)
splitframe.grid(row=4, pady=(15,0))

splitinput_label = ttk.Label(splitframe, text="Ordner auswählen: ")
splitinput_label.grid(row=0, column=0)

splitfile_label = ttk.Label(splitframe, width=50, anchor="center")
splitfile_label.config(text="...")
splitfile_label.grid(row=1, column=0)

splitdir_button = ttk.Button(splitframe, text="Durchsuchen")
splitdir_button.grid(row=2, column=0)

# BUTTON SECTION

buttonframe2 = ttk.Frame(root)
buttonframe2.grid(pady=15, row=5)

split_button = ttk.Button(buttonframe2)
split_button.grid(row=0, column=0)
split_button.configure(text="Split NOW!")

splitoutdir_button = ttk.Button(buttonframe2, text="Ausgabeordner öffnen")
splitoutdir_button.grid(row=0, column=1)

# Beenden-Button unten rechts

style = ttk.Style()
style.configure('redBTN.TButton', background='red', foreground='red')

quit_button = ttk.Button(root, text="Beenden", command=root.destroy, style='redBTN.TButton')
quit_button.grid(row=6, column=0, sticky=tkinter.E, pady=(15 ,0))

root.mainloop()
