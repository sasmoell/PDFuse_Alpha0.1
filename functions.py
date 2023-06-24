# Dieses Modul verwendet PyPDF (Version 3.11.0)
# Copyright (c) 2006-2008, Mathieu Fenniak
# Some contributions copyright (c) 2007, Ashish Kulkarni <kulkarni.ashish@gmail.com>
# Some contributions copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>
# Lizenziert unter der BSD 3-Clause Lizenz.
#
# Dieses Modul verwendet die Requests-Bibliothek (https://requests.readthedocs.io/).
# Requests ist unter der Apache-Lizenz 2.0 (https://www.apache.org/licenses/LICENSE-2.0) lizenziert.

import os
import subprocess
import requests
import webbrowser
import tkinter as tk
from tkinter import messagebox
from pypdf import PdfWriter, PdfReader

current_version = "0.1.2306" # Korrekte Angabe ist wichtig um auf Updates zu prüfen.

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


def ordner_pruefen_und_erstellen(pfad):
    if not os.path.exists(pfad):
        abfrage_box = tk.messagebox.askyesno(title="Frage",
                                             message=f"Der Ordner {pfad} ist nicht vorhanden. Soll er erstellt werden?")
        if abfrage_box:
            try:
                os.makedirs(pfad)
                gen_message_info("Info", f"Der Ordner {pfad} wurde erstellt.")
            except OSError:
                gen_error("Fehler", f"Der Ordner {pfad} konnte nicht erstellt werden.")


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
                      "Ordner konnte nicht erstellt werden.")

    for i in pdf_dateien:
        dateipfad = eingabe_ordner + "/" + i  # FOR-Schleife setzt den Dateipfad für den Merger zusammen
        merger.append(dateipfad)

    merger.write(ausgabe_datei)
    merger.close()

    tk.messagebox.showinfo(title="Info", message="Die Datei wurde erstellt.")


# Funktionen für PDFSplitter

split_output_ordner = "output/splits"

def pdf_splitten(quelldatei, split_output_ordner):
    with open(quelldatei, 'rb') as file:
        pdf = PdfReader(file)

        ordner_pruefen_und_erstellen("output/splits")

        # PDF-Datei in einzelne Seiten aufteilen
        for page_number, page in enumerate(pdf.pages):
            output_pdf = PdfWriter()
            output_pdf.add_page(page)

            # Speichere jede Seite als separate PDF-Datei
            output_filename = os.path.join(split_output_ordner, f'page_{page_number + 1}.pdf')
            with open(output_filename, 'wb') as output_file:
                output_pdf.write(output_file)

        gen_message_info("Hinweis", f"Dateien im Ordner {split_output_ordner} erstellt.")

# Funktionen für Update-Prüfung

update_pageurl = "https://mark42.de/fuser/alpha/"
def update_seite_oeffnen():
    webbrowser.open(update_pageurl)
def version_online_pruefen():
    vers_url = "https://mark42.de/fuser/alpha/release.txt"
    version = requests.get(vers_url)
    try:
        if version.status_code == 200:
            content = version.text
            return content
    except:
        gen_error("Fehler", "Die Updateprüfung ist fehlgeschlagen.")

def update_check():
    versionsnummer = version_online_pruefen()
    if versionsnummer != current_version:
        gen_message_info("Neue Version", "Es ist eine neue Version verfügbar!")
        print("Update vorhanden")
    else:
        gen_message_info("Version aktuell", "Sie arbeiten bereits mit der aktuellsten Version.")
        print("Kein Update vorhanden")
