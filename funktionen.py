######################################################################################
### Author: Sascha Möller, 2023 ######################################################
### Contact: sasmoell@t-online.de #### With great power comes great responsibility ###
### PDFuse Alpha 0.1 #################################################################
######################################################################################

# Dieses Modul verwendet PyPDF (Version 3.11.0)
# Copyright (c) 2006-2008, Mathieu Fenniak
# Some contributions copyright (c) 2007, Ashish Kulkarni <kulkarni.ashish@gmail.com>
# Some contributions copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>
# Lizenziert unter der BSD 3-Clause Lizenz.
#
# Dieses Modul verwendet die Requests-Bibliothek (https://requests.readthedocs.io/).
# Requests ist unter der Apache-Lizenz 2.0 (https://www.apache.org/licenses/LICENSE-2.0) lizenziert.

import os
import requests
import subprocess
import tkinter as tk
import webbrowser
from tkinter import messagebox
from pypdf import PdfWriter, PdfReader
import logging

# Konfiguration der Log-Datei
logging.basicConfig(filename="protokoll.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

# Wichtig für die Update-Prüfung; Wird verwendet in der Funktion update_check()
current_version = "0.1.2306"


# # # # # # Allgemeine (Fehler)Meldungen # # # # # #

# Titel und die Nachricht können als String-Argument übergeben werden.

# Fehlermeldung mit Protokollierung
def gen_error(titel, message):
    """
    Generische Fehlermeldung mit Log-Funktion auf Debug-Level. Titel und Text werden als Parameter übergeben. Die Fehlermeldung erscheint als Tk.Messagebox.
    :param titel:
    :param message:
    :return:
    """
    tk.messagebox.showerror(title=titel, message=message)
    logging.debug("%s: %s", titel, message)


# Allgemeiner Hinweis
def gen_message_info(titel, message):
    """
    Generischer Hinweis. Titel und Text werden als Parameter übergeben. Die Meldung erscheint als Tk.Messagebox.
    :param titel:
    :param message:
    :return:
    """
    tk.messagebox.showinfo(title=titel, message=message)


# Frage mit JA/NEIN Auswahl
def gen_yesno(titel, message):
    """
    Generische Abfrage JA/NEIN. Titel und Text werden als Parameter übergeben. Die Abfrage erscheint als Tk.Messagebox.
    :param titel:
    :param message:
    :return:
    """
    tk.messagebox.askyesno(title=titel, message=message)


# # # # # # Allgemeine Funktionen # # # # # #

# Explorer öffnen. Exceptions für unterschiedliche Betriebssysteme.
def ordner_oeffnen(pfad):
    """
    Die Funktion verwendet subprocess, um über den File-Explorer einen Ordner aufzurufen. Auch wenn PDFuser auf macOS oder Linux noch nicht lauffähig ist, sind hier bereits subprocess-Routinen für die Betriebssysteme integriert.
    :param pfad:
    :return:
    """
    try:
        subprocess.Popen(f'explorer {pfad}')  # windows
    except FileNotFoundError:
        try:
            subprocess.Popen(['open', pfad])  # macOS
        except OSError:
            subprocess.Popen(['xdg-open', pfad])  # Linux


# Existenzprüfung Dateipfad. Falls nicht vorhanden: Abfrage, ob Pfad erstellt werden soll.
# TODO abfrage_box ersetzen durch gen_yesno?
def ordner_pruefen_und_erstellen(pfad):
    """
    Hilfs-Funktion: Diese Funktion wird nur innerhalb einer anderen Funktion aufgerufen. Z.B. in der Funktion ausgabeordner_anlegen()
    :param pfad:
    :return:
    """
    if not os.path.exists(pfad):
        abfrage_box = tk.messagebox.askyesno(title="Frage",
                                             message=f"Der Ordner {pfad} ist nicht vorhanden. Soll er erstellt werden?")
        if abfrage_box:
            try:
                os.makedirs(pfad)
                gen_message_info("Info", f"Der Ordner {pfad} wurde erstellt.")
            except OSError:
                gen_error("Fehler", f"Der Ordner {pfad} konnte nicht erstellt werden.")


# Existenzprüfung für den Standard-Ausgabeordner. Falls nicht vorhanden: ordner_pruefen_und_erstellen()
def ausgabeordner_anlegen():
    """
    Die Standard Ausgabe-Ordner werden mit dieser Funktion angelegt. Es erfolgt eine Existenzprüfung. Wenn die Standard-Ausgabe-Ordner nicht vorhanden sind, wird jeweils die Hilfsfunktion ordner_pruefen_und_erstellen() aufgerufen.
    :return:
    """
    if os.path.exists("output/mergeoutput") and os.path.exists("output/newFiles"):
        gen_message_info("Info", "Die Ordner existieren bereits.")
    else:
        try:
            ordner_pruefen_und_erstellen("output/mergeoutput")
            ordner_pruefen_und_erstellen("output/newFiles")
        except OSError:
            gen_error("Fehler", "Erstellen war nicht möglich.")


# # # # # # PDFuser Funktionen für PDFs zusammenfassen # # # # # #

# Funktionen für PDFuser. Hier wird der PdfWriter aus pypdf genutzt. Da pypdf die grundlegendste Bibliothek des Projektes ist, wird hier etwas ausführlicher kommentiert.
def pdf_zusammenfassen(eingabe_ordner, ausgabe_datei):
    """
    Diese Funktion nutzt aus der Bibliothek PyPDF die Funktion PdfWriter. Die Instanz wurde mit "merger" deklariert. Im ersten Schritt werden alle Dateien aus dem Eingabeordner in eine Liste gesammelt mit einer List-Comprehension. Im nächsten Schritt wird überprüft, ob der Standard-Ausgabeordner existiert. Falls nicht, wird versucht ihn zu erstellen. Die folgende erneute FOR-Schleife dient dazu, die Dateipfad zu erstellen, welche dem PdfWriter-Objekt (merger) hinzugefügt werden. Mit der write-Methode wird nun die Datei geschrieben, die alle PDF-Dokumente beinhaltet. Abschließend wird sichergestellt, dass alle Ressourcen mit der close-Methode wieder freigegeben werden und eine Bestätigungsmeldung erscheint.
    :param eingabe_ordner:
    :param ausgabe_datei:
    :return:
    """
    merger = PdfWriter()  # Erstellt ein PdfWriter-Objekt aus der Klasse zum Zusammenführen der PDFs.

    pdf_dateien = [d for d in os.listdir(eingabe_ordner) if
                   d.endswith(
                       ".pdf")]  # Erstellt eine Liste der PDF-Dateien im Eingabeordner mit einer List Comprehension. Die For-Schleife wird direkt in der Liste ausgeführt.

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

# Ausgabeordner für gesplittete PDF-Dateien
split_output_ordner = "output/newFiles"


def pdf_splitten(quelldatei, split_output_ordner):
    """
    In dieser Funktion wird der PdfReader UND PdfWriter aus pypdf genutzt. Die Quelldatei wird im binären Lesemodus geöffnet und an den PdfReader übergeben. Mit einer FOR-Schleife und der page-Methode werden die einzelnen Seiten gelistet und an den PdfWriter übergeben. Da die Quelldatei im Lesemodus 'rb' geöffnet wird, ist an dieser Stelle sichergestellt, dass die Ursprungsdatei nicht verändert wird. Erst die Liste der einzelnen Seiten wird im Schreibmodus verwendet.
    :param quelldatei:
    :param split_output_ordner:
    :return:
    """
    with open(quelldatei, 'rb') as file:  # öffnen der quelldatei im binären Modus 'rb'
        pdf = PdfReader(file)  # Erstellt ein PdfReader-Objekt aus der Klasse und übergibt die quelldatei (as file)

        ordner_pruefen_und_erstellen("output/newFiles")

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


# URL der Onlinedokumentation
update_pageurl = "https://mark42.de/"


def update_seite_oeffnen():
    """
    Öffnet die Onlinedokumentation im Standard-Browser
    :return:
    """
    webbrowser.open(update_pageurl)


# Hilfsfunktion: Ermitteln der Online-Versionsnummer
def onlineversion_pruefen():
    """
    Die Variable vers_url beinhaltet URL zu der Textdatei release.dat. Die Datei beinhaltet ausschließlich eine Versionsnummer, welche mit der aktuell verwendeten Version verglichen wird. Diese Funktion fragt den Status der Datei ab, um die Erreichbarkeit abzufragen. Wenn der Status 200 lautet, wird der Inhalt (Versionsnummer) zurückgegeben. Lautet der Status !=200, wird eine Fehlermeldung ausgegeben. Unabhängig vom Erfolg, wird die Datei am Ende der Funktion geschlossen.
    :return: Versionsnummer (content)
    """
    vers_url = "https://mark42.de/fuser/alpha/release.dat"
    version = requests.get(vers_url)
    try:
        if version.status_code == 200:
            content = version.text
            return content
        elif version.status_code != 200:  # NEU
            gen_error("Fehler", "Fehler beim Abrufen der Versionsnummer")
            content = None
            return content
    except FileNotFoundError:
        gen_error("Fehler", "Die Updateprüfung ist fehlgeschlagen.")
    finally:
        version.close()


# Vergleich die Online-Versionsnummer mit der lokalen Versionsnummer
def update_check():
    """
    Die Hilfsfunktion onlineversion_pruefen() wird ausgeführt. Die ermittelte Online-Versionsnummer wird mit der lokalen Versionsnummer verglichen. Je nach Ergebnis, wird eine Update-Meldung angezeigt.
    :return:
    """
    versionsnummer = onlineversion_pruefen()
    if versionsnummer is None:
        gen_error("Fehler", "Versionsnummer konnte nicht geprüft werden.")
        return
    elif versionsnummer != current_version:
        gen_message_info("Neue Version",
                         f"Version {versionsnummer} ist verfügbar! - Unter Hilfe -> Update Download finden Sie weitere Informationen.")
        print("Update vorhanden")
    else:
        gen_message_info("Version aktuell", "Sie arbeiten bereits mit der aktuellsten Version.")
        print("Kein Update vorhanden")
