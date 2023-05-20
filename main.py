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
root.minsize(800, 600)
root.maxsize(800, 600)

title_label = ttk.Label(root, text="PDFuser", font=("Arial", 22))
title_label.pack(pady=(10, 10))

desc_label = ttk.Label(root,
                       text="Bitte wählen Sie zunächst den Ordner aus, in dem sich die PDF-Dateien befinden um sie zusammenzuführen.")
desc_label.pack(pady=(10, 10))

# Ordnerauswahl Input Bereich
dir_frame = ttk.Frame(root)
dir_frame.pack(side="top")

input_label = ttk.Label(dir_frame, text="Ordner auswählen: ")
input_label.pack(side="top", anchor="nw")

file_entry = ttk.Entry(dir_frame, width=80)
file_entry.insert(0, "C:/")
file_entry.pack(side="left")

dir_button = ttk.Button(dir_frame, text="...", command=set_inputdir)
dir_button.pack(side="left")

# Button Section

buttonframe1 = ttk.Frame(root)
buttonframe1.pack(side="top", pady=(10, 10), )

merge_button = ttk.Button(buttonframe1, command=wmerge_pdfs)
merge_button.pack(side="left")
merge_button.configure(text="Dateien zusammenführen", padding=10)

outdir_button = ttk.Button(buttonframe1, text="Ausgabeordner öffnen", command=wopendir_output)
outdir_button.pack(side="left")
outdir_button.config(padding=10)

# SPLIT BEREICH

splitframe = ttk.Frame(root)
splitframe.pack(side="top")

title_label = ttk.Label(splitframe, text="PDFSplitter", font=("Arial", 22))
title_label.pack(pady=(10, 10))

splitdesc_label = ttk.Label(splitframe, text="Bitte wählen Sie zunächst die Datei aus, um sie zu splitten.")
splitdesc_label.pack(pady=(10, 10))

splitinput_label = ttk.Label(splitframe, text="Datei auswählen: ")
splitinput_label.pack(side="top", anchor="nw")

splitfile_entry = ttk.Entry(splitframe, width=80)
splitfile_entry.insert(0, "C:/")
splitfile_entry.pack(side="left")

splitdir_button = ttk.Button(splitframe, text="...", command=set_inputfile)
splitdir_button.pack(side="left")

buttonframe2 = ttk.Frame(root)
buttonframe2.pack(side="top", pady=(10, 10))

split_button = ttk.Button(buttonframe2, command=wsplit_pdf)
split_button.pack(side="left")
split_button.configure(text="Datei splitten", padding=10)

splitoutdir_button = ttk.Button(buttonframe2, text="Ausgabeordner öffnen", command=wopendir_soutput)
splitoutdir_button.pack(side="left")
splitoutdir_button.config(padding=10)

# Gruppe der Buttons unten rechts
bright_frame = ttk.Frame(root)
bright_frame.pack(side="bottom", anchor="se", pady=(10, 10), padx=(0, 10))

quit_button = ttk.Button(bright_frame, text="Beenden", command=root.destroy)
quit_button.pack(side="left")

root.mainloop()
