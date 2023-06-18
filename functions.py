import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from pypdf import PdfWriter


# Generische Fehlermeldungen
def gen_error(titel, message):
    tk.messagebox.showerror(title=titel, message=message)


def gen_message_info(titel, message):
    tk.messagebox.showinfo(title=titel, message=message)


def gen_yesno(titel, message):
    tk.messagebox.askyesno(title=titel, message=message)


# Allgemeine Funktionen
def ordner_oeffnen(pfad):
    try:
        subprocess.Popen(f'explorer {pfad}')
    except FileNotFoundError:
        try:
            subprocess.Popen(['open', pfad])
        except OSError:
            subprocess.Popen(['xdg-open', pfad])


# Funktionen für PDFuser
def pdf_zusammenfassen(eingabe_ordner, ausgabe_datei):
    merger = PdfWriter()

    pdf_dateien = [d for d in os.listdir(eingabe_ordner) if
                   d.endswith(".pdf")]  # Listet alle Dateien mit der *.pdf-Endung im Ordner eingabe_ordner auf

    if not os.path.exists("output/mergeoutput"):  # Überprüft ob der Ordner nicht vorhanden
        try:
            os.makedirs("output/mergeoutput")  # Versucht Ordner zu erstellen
        except OSError:
            gen_error("Fehler",
                      "Ordner konnte nicht erstellt werden.")  # Wirft eine Fehlermeldung, wenn der Ordner nicht erstellt werden konnte

    for i in pdf_dateien:
        dateipfad = eingabe_ordner + "/" + i  # FOR-Schleife setzt den Dateipfad für den Merger zusammen
        merger.append(dateipfad)

    merger.write(ausgabe_datei)
    merger.close()

    tk.messagebox.showinfo(title="Info", message="Die Datei wurde erstellt.")


def ordner_pruefen_und_erstellen(pfad):
    if not os.path.exists(pfad):
        abfrage_box = tk.messagebox.askyesno(title="Frage", message=f"Der Ordner {pfad} ist nicht vorhanden. Soll er erstellt werden?")
        if abfrage_box:
            try:
                os.makedirs(pfad)
                gen_message_info("Info", f"Der Ordner {pfad} wurde erstellt.")
            except OSError:
                gen_error("Fehler", f"Der Ordner {pfad} konnte nicht erstellt werden.")
