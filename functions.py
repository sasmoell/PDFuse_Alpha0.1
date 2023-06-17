import os
from pypdf import PdfReader, PdfMerger, PdfWriter
import tkinter as tk
from tkinter import messagebox, filedialog

# Funktionen um PDFs zusammenzuführen
def pdf_zusammenfassen(eingabe_ordner, ausgabe_datei):
    merger = PdfWriter()

    pdf_dateien = [d for d in os.listdir(eingabe_ordner) if d.endswith(".pdf")] # Listet alle Dateien mit der *.pdf-Endung im Ordner eingabe_ordner auf

    if not os.path.exists("output"): # Überprüft ob der Ordner nicht vorhanden
        try:
            os.makedirs("output") # Versucht Ordner zu erstellen
        except:
            tk.messagebox.showerror(title="Fehler", message="Ordner konnte nicht erstellt werden.") # Wirft eine Fehlermeldung, wenn der Ordner nicht erstellt werden konnte

    for i in pdf_dateien:
        dateipfad = eingabe_ordner + "/" + i # FOR-Schleife setzt den Dateipfad für den Merger zusammen
        merger.append(dateipfad)

    merger.write(ausgabe_datei)
    merger.close()

    tk.messagebox.showinfo(title="Info", message="Die Datei wurde erstellt.")