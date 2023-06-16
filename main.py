import tkinter
import tkinter as tk
from tkinter import ttk, filedialog
from modul1 import opendir_output, merge_pdfs, split_pdf, output_file, soutput_directory

def wopendir_output():
    opendir_output()

def wmerge_pdfs():
    merge_pdfs(inputdir_path, output_file)

def wsplit_pdf():
    split_pdf(input_file, soutput_directory)

def winput_file():
    input_file()

def wopendir_soutput():
    opendir_output()

def set_inputdir():
    global inputdir_path
    inputdir_path = filedialog.askdirectory()
    if inputdir_path:
        print("Ausgewählter Ordner:", inputdir_path)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, inputdir_path)
        return inputdir_path

def set_inputfile():
    global input_file
    input_file = filedialog.askopenfilename()
    if input_file:
        print("Ausgewählte Datei:", input_file)
        splitfile_entry.delete(0, tk.END)
        splitfile_entry.insert(0, input_file)
    return input_file

# GUI mit Tkinter

root = tk.Tk()
root.title("PDFuse Alpha 0.1.0523")
root.config(pady=20, padx=20)
root.resizable(False, False)

#MENÜ
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Datei", menu=filemenu)

filemenu.add_command(label="Ausgabeordner")
filemenu.add_separator()
filemenu.add_command(label="Ordner öffnen")
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=root.destroy)

root.config(menu=menubar)

#PDFuser Kopfbereich
headframe = ttk.Frame(root)
headframe.grid(pady=(0, 15), row=0)

title_label = ttk.Label(headframe, text="PDFuser", font=("Arial", 22))
title_label.grid()

desc_label = ttk.Label(headframe, text="Bitte Ordner auswählen, in dem sich die PDF-Dateien befinden.")
desc_label.grid()

# Ordnerauswahl Input Bereich
dir_frame = ttk.Frame(root)
dir_frame.grid(row=1)

input_label = ttk.Label(dir_frame, text="Ordner auswählen: ")
input_label.grid(row=1, column=0)

file_entry = ttk.Entry(dir_frame, width=50)
file_entry.insert(0, "C:/")
file_entry.grid(row=2, column=0)

dir_button = ttk.Button(dir_frame, text="Durchsuchen", command=set_inputdir)
dir_button.grid(row=2, column=1)

# Button Section (PDFuser)
buttonframe1 = ttk.Frame(root)
buttonframe1.grid(row=2, pady=15)

merge_button = ttk.Button(buttonframe1, command=wmerge_pdfs)
merge_button.grid(row=0, column=0)

merge_button.configure(text="Fuse NOW!")
outdir_button = ttk.Button(buttonframe1, text="Ausgabeordner öffnen", command=wopendir_output)
outdir_button.grid(row=0, column=1)

#PDFSplitter Kopfbereich
headframe2 = ttk.Frame(root)
headframe2.grid(pady=(15, 0), row=3)

title_label = ttk.Label(headframe2, text="PDFSplitter", font=("Arial", 22))
title_label.grid()

splitdesc_label = ttk.Label(headframe2, text="Bitte wählen Sie zunächst die Datei aus.")
splitdesc_label.grid()


# SPLIT BEREICH
splitframe = ttk.Frame(root)
splitframe.grid(row=4, pady=(15,0))

splitinput_label = ttk.Label(splitframe, text="Datei auswählen: ")
splitinput_label.grid()

splitfile_entry = ttk.Entry(splitframe, width=50)
splitfile_entry.insert(0, "C:/")
splitfile_entry.grid(row=0, column=0)

splitdir_button = ttk.Button(splitframe, text="Durchsuchen", command=set_inputfile)
splitdir_button.grid(row=0, column=1)

# BUTTON SECTION

buttonframe2 = ttk.Frame(root)
buttonframe2.grid(pady=15, row=5)

split_button = ttk.Button(buttonframe2, command=wsplit_pdf)
split_button.grid(row=0, column=0)
split_button.configure(text="Split NOW!")

splitoutdir_button = ttk.Button(buttonframe2, text="Ausgabeordner öffnen", command=wopendir_soutput)
splitoutdir_button.grid(row=0, column=1)
#splitoutdir_button.config()

# Beenden-Button unten rechts

style = ttk.Style()
style.configure('redBTN.TButton', background='red', foreground='red')

quit_button = ttk.Button(root, text="Beenden", command=root.destroy, style='redBTN.TButton')
quit_button.grid(row=6, column=0, sticky=tkinter.E, pady=(15 ,0))

root.mainloop()
