# Dieses Modul verwendet PyPDF (Version 3.11.0)
# Copyright (c) 2006-2008, Mathieu Fenniak
# Some contributions copyright (c) 2007, Ashish Kulkarni <kulkarni.ashish@gmail.com>
# Some contributions copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>
# Lizenziert unter der BSD 3-Clause Lizenz.
#
# Dieses Modul verwendet die Requests-Bibliothek (https://requests.readthedocs.io/).
# Requests ist unter der Apache-Lizenz 2.0 (https://www.apache.org/licenses/LICENSE-2.0) lizenziert.

import os, subprocess, requests, webbrowser
import tkinter as tk
from tkinter import messagebox
from pypdf import PdfWriter, PdfReader

current_version = "0.1.2306"  # Korrekte Angabe ist wichtig um auf Updates zu prüfen.


# # # # # # Allgemeine (Fehler)Meldungen # # # # # #

# Generische Fehlermeldungen: Es werden im Programm diverse unter Umständen Fenster für Fragen, Fehler und Hinweise ausgegeben. Um den Umgang im Code damit etwas zu vereinfachen, wurden sie hier als Funktion definiert. Der Titel und die Nachricht können als String-Argument übergeben werden.

def gen_error(titel, message):
    tk.messagebox.showerror(title=titel, message=message)


# Allgemeiner Hinweis
def gen_message_info(titel, message):
    tk.messagebox.showinfo(title=titel, message=message)


# Frage mit JA/NEIN Auswahl
def gen_yesno(titel, message):
    tk.messagebox.askyesno(title=titel, message=message)


# # # # # # Allgemeine Funktionen # # # # # #

# Mit der Bibliothek subprocess wird im Falle eines Windows-OS versucht der Explorer zu öffnen. Für den Fall, dass es nicht funktioniert wird eine macOS-Umgebung angenommen und der "open"-Befehl versucht auszuführen. Sollte auch das noch fehlschlagen, wird ein Linux-OS angenommen.
def ordner_oeffnen(pfad):
    try:
        subprocess.Popen(f'explorer {pfad}')
    except FileNotFoundError:
        try:
            subprocess.Popen(['open', pfad])
        except OSError:
            subprocess.Popen(['xdg-open', pfad])


# Die Funktion überprüft zunächst, ob ein Pfad (hier ein Argument, welches übergeben werden kann) vorhanden ist. Falls der Pfad nicht vorhanden ist, wird gefragt, ob er erstellt werden soll. Anschließend wird er je nach Auswahl erstellt oder nicht.
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


# # # # # # PDFuser Funktionen für PDFs zusammenfassen # # # # # #

# Funktionen für PDFuser. Hier wird der PdfWriter aus pypdf genutzt. Da pypdf die grundlegendste Bibliothek des Projektes ist, wird hier etwas ausführlicher kommentiert.
def pdf_zusammenfassen(eingabe_ordner, ausgabe_datei):
    merger = PdfWriter()  # Erstellt ein PdfWriter-Objekt aus der Klasse zum Zusammenführen der PDFs.

    pdf_dateien = [d for d in os.listdir(eingabe_ordner) if
                   d.endswith(".pdf")]  # Erstellt eine Liste der PDF-Dateien im Eingabeordner mit einer List Comprehension. Die For-Schleife wird direkt in der Liste ausgeführt.

    if not os.path.exists("output/mergeoutput"):  # Überprüft, ob der Ausgabeordner existiert.
        try:
            os.makedirs("output/mergeoutput")  # Versucht den Ordner zu erstellen, falls er nicht existiert.
        except OSError:
            gen_error("Fehler",
                      "Ordner konnte nicht erstellt werden.")

    for i in pdf_dateien:  # Schleife über jede PDF-Datei im Eingabeordner.
        dateipfad = eingabe_ordner + "/" + i  # Erstellt den vollständigen Dateipfad.
        merger.append(dateipfad)  # Fügt die PDF-Datei bzw. den Pfad zum PdfWriter-Objekt hinzu.

    merger.write(ausgabe_datei)  # Schreibt die zusammengeführten PDFs in die Ausgabedatei.
    merger.close()  # Wer es aufmacht, muss es auch wieder schließen! ;-)

    tk.messagebox.showinfo(title="Info",
                           message="Die Datei wurde erstellt.")  # Zeigt eine Infomeldung an, dass die Datei erstellt wurde.


# # # # # # PDFuser Funktionen für PDFs teilen (splitten) # # # # # #

# Funktionen für PDFSplitter. Hier wird der PdfReader aus pypdf genutzt. Da pypdf die grundlegendste Bibliothek des Projektes ist, wird hier etwas ausführlicher kommentiert.

split_output_ordner = "output/splits"


def pdf_splitten(quelldatei, split_output_ordner):
    with open(quelldatei, 'rb') as file:  # öffnen der quelldatei im binären Modus 'rb'
        pdf = PdfReader(file)  # Erstellt ein PdfReader-Objekt aus der Klasse und übergibt die quelldatei (as file)

        ordner_pruefen_und_erstellen("output/splits")  # Funktion ist oben beschrieben und kommentiert

        # PDF-Datei in einzelne Seiten aufteilen
        for page_number, page in enumerate(
                pdf.pages):  # Jede Seite der Datei wird mit der FOR-Schleife aufgelistet um darauf zugreifen zu können
            output_pdf = PdfWriter()  # Der PdfWriter wird erstellt
            output_pdf.add_page(page)  # Die Seiten werden an den PdfWriter übergeben

            # Speichere jede Seite als separate PDF-Datei
            output_filename = os.path.join(split_output_ordner, f'page_{page_number + 1}.pdf')
            with open(output_filename, 'wb') as output_file:
                output_pdf.write(output_file)

        gen_message_info("Hinweis", f"Dateien im Ordner {split_output_ordner} erstellt.")


# # # # # # Funktionen für Update-Prüfung # # # # # #

update_pageurl = "https://mark42.de/fuser/alpha/"  # Online Ressource


def update_seite_oeffnen():  # Wird aktuell nicht verwendet. Öffnet die Online-Dokumentation vom Programm.
    webbrowser.open(update_pageurl)


# Versucht die Datei release.txt online zu erreichen und die Versionsnummer zu ermitteln. Die Bibliothek Requests kommt zum Einsatz um den Status der Datei zu ermitteln.
def versionsnummer_online_pruefen():
    vers_url = "https://mark42.de/fuser/alpha/release.txt"
    version = requests.get(vers_url)
    try:
        if version.status_code == 200:
            content = version.text
            return content
        elif version.status_code != 200:  # NEU
            gen_error("Fehler", "Fehler beim Abrufen der Versionsnummer")
            content = None
            return content
    except:
        gen_error("Fehler", "Die Updateprüfung ist fehlgeschlagen.")
    finally: # Python3 S. 409 / Verwendet in U-Einheit 20230703 / Wer etwas öffnet, muss es auch schließen! ;-)
        version.close()


# Prüft ob die Onlineversionsnummer verfügbar ist und vergleicht die aktuelle Versionsnummer mit der Onlineversionsnummer. Wenn die Nummern unterschiedlich sind, wird ein Update gemeldet.
def update_check():
    versionsnummer = versionsnummer_online_pruefen()
    if versionsnummer == None:
        gen_error("Fehler", "Versionsnummer konnte nicht geprüft werden.")
        return
    elif versionsnummer != current_version:
        gen_message_info("Neue Version",
                         f"Version {versionsnummer} ist verfügbar! - Unter Hilfe -> Update Download finden Sie weitere Informationen.")
        print("Update vorhanden")
    else:
        gen_message_info("Version aktuell", "Sie arbeiten bereits mit der aktuellsten Version.")
        print("Kein Update vorhanden")
