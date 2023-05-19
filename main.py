import os
import subprocess
from PyPDF2 import PdfWriter, PdfMerger, PdfReader
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Setzt den Eingabeordner

inputdir_path = None

def set_inputdir():
    global inputdir_path
    inputdir_path = filedialog.askdirectory()
    if inputdir_path:
        print("Ausgewählter Ordner:", inputdir_path)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, inputdir_path)
        return inputdir_path

# Öffnet den Ausgabeordner im FileExplorer: /output im Hauptverzeichnis des Programms

output_directory = "output"

def opendir_output():
    try:
        subprocess.Popen(f'explorer {output_directory}')
    except FileNotFoundError:
        try:
            subprocess.Popen(['open', output_directory])
        except OSError:
            subprocess.Popen(['xdg-open', output_directory])

# Funktion PDFs zusammenführen

output_file = "output/merged.pdf"

def merge_pdfs(input_folder, output_file):
    merger = PdfMerger()

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]

    if not os.path.exists("output"):
        os.makedirs("output")

    for pdf_file in pdf_files:
        file_path = os.path.join(input_folder, pdf_file)
        merger.append(file_path)

    merger.write(output_file)
    merger.close()

    messagebox.showinfo("Hinweis!",
                        "Die Dateien wurden zusammengefügt. Das Ergebnis befindet sich im Ausgabeordner 'output' im Stammverzeichnis des Programms.")


# Funktionen für den Splitter
input_file = None


def set_inputfile():
    global input_file
    input_file = filedialog.askopenfilename()
    if input_file:
        print("Ausgewählte Datei:", input_file)
        splitfile_entry.delete(0, tk.END)
        splitfile_entry.insert(0, input_file)
    return input_file


def opendir_soutput():
    try:
        subprocess.Popen(f'explorer {soutput_directory}')
    except FileNotFoundError:
        try:
            subprocess.Popen(['open', soutput_directory])
        except OSError:
            subprocess.Popen(['xdg-open', soutput_directory])


soutput_directory = "splitout"

def split_pdf(input_file, soutput_directory):
    with open(input_file, 'rb') as file:
        pdf = PdfReader(file)

        # Erstelle den Ausgabeverzeichnis, wenn es nicht existiert
        if not os.path.exists(soutput_directory):
            os.makedirs(soutput_directory)

        # Teile die PDF-Datei in einzelne Seiten auf
        for page_number, page in enumerate(pdf.pages):
            output_pdf = PdfWriter()
            output_pdf.add_page(page)

            # Speichere jede Seite als separate PDF-Datei
            output_filename = os.path.join(soutput_directory, f'page_{page_number + 1}.pdf')
            with open(output_filename, 'wb') as output_file:
                output_pdf.write(output_file)

            messagebox.showinfo("Hinweis!",
                                "Die Dateien wurden gesplittet. Die Dateien befinden sich im Ausgabeordner 'splitout' im Stammverzeichnis des Programms.")

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
file_entry.insert(0, "Noch kein Ordner ausgewählt.")
file_entry.pack(side="left")
file_entry.focus()

dir_button = ttk.Button(dir_frame, text="...", command=set_inputdir)
dir_button.pack(side="left")

# Button Section

buttonframe1 = ttk.Frame(root)
buttonframe1.pack(side="top", pady=(10, 10), )

merge_button = ttk.Button(buttonframe1, command=lambda: merge_pdfs(inputdir_path, output_file))
merge_button.pack(side="left")
merge_button.configure(text="Dateien zusammenführen", padding=10)

outdir_button = ttk.Button(buttonframe1, text="Ausgabeordner öffnen", command=opendir_output)
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
splitfile_entry.insert(0, "Noch keine Datei ausgewählt.")
splitfile_entry.pack(side="left")
splitfile_entry.focus()

splitdir_button = ttk.Button(splitframe, text="...", command=set_inputfile)
splitdir_button.pack(side="left")

buttonframe2 = ttk.Frame(root)
buttonframe2.pack(side="top", pady=(10, 10))

split_button = ttk.Button(buttonframe2, command=lambda: split_pdf(input_file, soutput_directory))
split_button.pack(side="left")
split_button.configure(text="Datei splitten", padding=10)

splitoutdir_button = ttk.Button(buttonframe2, text="Ausgabeordner öffnen", command=opendir_soutput)
splitoutdir_button.pack(side="left")
splitoutdir_button.config(padding=10)

# Gruppe der Buttons unten rechts
bright_frame = ttk.Frame(root)
bright_frame.pack(side="bottom", anchor="se", pady=(10, 10), padx=(0, 10))

quit_button = ttk.Button(bright_frame, text="Beenden", command=root.destroy)
quit_button.pack(side="left")

root.mainloop()

# TODO Hier sind einige Vorschläge zur Optimierung deines Programms:
#
# 1. Vermeide den Einsatz globaler Variablen: In deinem Code verwendest du einige globale Variablen wie `inputdir_path`
# und `input_file`. Es ist jedoch empfehlenswert, den Einsatz globaler Variablen zu vermeiden, da dies zu unerwartetem
# Verhalten und Komplikationen führen kann. Stattdessen kannst du Funktionen verwenden, um die erforderlichen Werte
# zurückzugeben.
#
# 2. Verbessere die Lesbarkeit des Codes: Einige deiner Variablen- und Funktionsnamen könnten aussagekräftiger sein, um
# den Code besser lesbar zu machen. Zum Beispiel könntest du `set_inputdir` in `select_input_directory` umbenennen, um
# klarer zu machen, was die Funktion tut.
#
# 3. Verwende `os.path.join` für Dateipfade: Statt den Dateipfad manuell mit `/` zu verbinden, kannst du die Funktion
# `os.path.join` verwenden, um plattformunabhängige Dateipfade zu erstellen. Zum Beispiel: `output_file = os.path.join("output", "merged.pdf")`.
#
# 4. Verwende `os.makedirs` mit dem Parameter `exist_ok`: Anstatt zu überprüfen, ob der Ausgabeordner existiert, kannst
# du die Funktion `os.makedirs` mit dem Parameter `exist_ok=True` verwenden. Dadurch wird der Ordner nur dann erstellt,
# wenn er nicht bereits vorhanden ist.
#
# 5. Vermeide redundante Codeblöcke: In deinem Code gibt es einige ähnliche Codeblöcke, wie z.B. die Funktionen
# `opendir_output` und `opendir_soutput`. Du könntest diese Funktionalitäten in eine einzige Funktion extrahieren und
# die Werte für den Ordner und die Meldung als Parameter übergeben.
#
# 6. Trenne den Code in Funktionen und Klassen: Um den Code besser zu strukturieren und wartbarer zu machen, könntest
# du den Code in Funktionen und Klassen aufteilen. Jeder Funktions- oder Klassenblock könnte eine spezifische Aufgabe
# erfüllen, wie z.B. das Zusammenführen von PDFs oder das Splitten von PDF-Dateien.
#
# 7. Implementiere Fehlerbehandlung: In deinem Code fehlt die Behandlung von potenziellen Fehlern, z.B. wenn der
# Benutzer das Fenster zum Dateiauswählen schließt, ohne eine Datei auszuwählen. Es ist empfehlenswert,
# Fehlerbehandlungsmechanismen einzuführen, um solche Szenarien abzufangen und dem Benutzer entsprechende Rückmeldungen
# zu geben.
#
# 8. Verbessere die Benutzerfreundlichkeit: Du könntest die Benutzerfreundlichkeit deiner Anwendung verbessern, indem du
# aussagekräftige Meldungen anzeigst, die den Benutzer über den Status der Operationen informieren. Du könntest auch
# Fortschrittsanzeigen oder eine bessere Fehlerbehandlung implementieren, um dem Benutzer eine angenehmere Erfahrung zu bieten.
