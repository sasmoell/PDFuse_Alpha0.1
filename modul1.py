import os
import subprocess
from PyPDF2 import PdfWriter, PdfMerger, PdfReader
from tkinter import messagebox

inputdir_path = None

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

output_file = "output/merged.pdf"


# Funktion PDFs zusammenführen

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

        # Ausgabeverzeichnis erstellen
        if not os.path.exists(soutput_directory):
            os.makedirs(soutput_directory)

        # PDF-Datei in einzelne Seiten aufteilen
        for page_number, page in enumerate(pdf.pages):
            output_pdf = PdfWriter()
            output_pdf.add_page(page)

            # Speichere jede Seite als separate PDF-Datei
            output_filename = os.path.join(soutput_directory, f'page_{page_number + 1}.pdf')
            with open(output_filename, 'wb') as output_file:
                output_pdf.write(output_file)

            messagebox.showinfo("Hinweis!",
                                "Die Dateien wurden gesplittet. Die Dateien befinden sich im Ausgabeordner 'splitout' im Stammverzeichnis des Programms.")