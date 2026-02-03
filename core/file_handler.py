# -*- coding: utf-8 -*-
"""
Modul für die Dateiverarbeitung (I/O).

Der FileHandler kümmert sich um das Einlesen von externen Dokumenten (PDF, DOCX),
extrahiert deren Textinhalte und führt eine erste Bereinigung (Preprocessing) durch,
bevor die Daten an die Analyse weitergegeben werden.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

import re
from pathlib import Path
from typing import Optional

import PyPDF2
import docx


class FileHandler:
    """
    Klasse zur Handhabung von Datei-Importen und Text-Extraktion.

    Attributes:
        current_file_path (Optional[Path]): Der Pfad zur aktuell geladenen Datei.
        raw_text (str): Der unveränderte Originaltext aus der Datei.
        clean_text (str): Der bereinigte Text nach dem Preprocessing.
    """

    def __init__(self) -> None:
        """Initialisiert den FileHandler mit leeren Zuständen."""
        self.current_file_path: Optional[Path] = None
        self.raw_text: str = ""
        self.clean_text: str = ""

    def set_file_path(self, path: str) -> bool:
        """
        Setzt den Pfad zur zu analysierenden Datei.

        Validiert, ob der Pfad existiert und speichert ihn als Path-Objekt.

        Args:
            path (str): Der absolute oder relative Dateipfad.

        Returns:
            bool: True, wenn die Datei existiert, sonst False.
        """
        if not path:
            return False
            
        p = Path(path)
        if p.exists() and p.is_file():
            self.current_file_path = p
            return True
        
        return False

    def get_filename(self) -> str:
        """
        Gibt den reinen Dateinamen zurück.

        Returns:
            str: Dateiname (z. B. 'lastenheft.pdf') oder Platzhaltertext.
        """
        if self.current_file_path:
            return self.current_file_path.name
        return "Keine Datei"

    def get_full_path(self) -> str:
        """
        Gibt den absoluten Pfad der aktuellen Datei als String zurück.

        Returns:
            str: Der absolute Pfad oder ein leerer String.
        """
        if self.current_file_path:
            return str(self.current_file_path.absolute())
        return ""

    def read_text(self) -> str:
        """
        Liest den Textinhalt basierend auf der Dateiendung ein.

        Unterstützt aktuell .pdf und .docx Dateien.
        
        Hinweis: .doc (altes Word-Format) wird von python-docx nicht unterstützt.

        Returns:
            str: Der extrahierte Text oder eine Fehlermeldung (beginnend mit "Fehler:").
        """
        if not self.current_file_path:
            return "Fehler: Kein Dateipfad gesetzt."

        try:
            # Dateiendung prüfen (kleingeschrieben)
            suffix = self.current_file_path.suffix.lower()

            if suffix == ".pdf":
                text = self._read_pdf()
            elif suffix == ".docx":
                text = self._read_docx()
            else:
                return f"Fehler: Dateiformat '{suffix}' wird nicht unterstützt."

            self.raw_text = text
            return text

        except Exception as e:
            return f"Fehler beim Lesen der Datei: {str(e)}"

    def preprocess_text(self) -> str:
        """
        Führt eine Textbereinigung auf den Rohdaten durch.

        Bereinigungen:
        1. Mehrfache Leerzeichen/Zeilenumbrüche zu einem Leerzeichen reduzieren.
        2. Seitenzahlen entfernen (Muster: 'Seite X von Y').
        3. Silbentrennung korrigieren (Wort- trennung -> Worttrennung).

        Returns:
            str: Der bereinigte Text.
        """
        if not self.raw_text:
            return ""

        text = self.raw_text

        # 1. Silbentrennung am Zeilenende zusammenfügen
        # Beispiel: "Anforde- \n rung" -> "Anforderung"
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

        # 2. Seitenzahlen entfernen (z.B. "Seite 1 von 10")
        text = re.sub(r'(?i)Seite\s+\d+\s+von\s+\d+', '', text)

        # 3. Whitespace normalisieren (Tabs, Newlines -> 1 Leerzeichen)
        text = re.sub(r'\s+', ' ', text)

        self.clean_text = text.strip()
        return self.clean_text

    # -------------------------------------------------------------------------
    # Private Hilfsmethoden
    # -------------------------------------------------------------------------

    def _read_pdf(self) -> str:
        """Interner Helper zum Lesen von PDFs mittels PyPDF2."""
        text = ""
        # 'rb' mode ist wichtig für PDF
        with open(self.current_file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    def _read_docx(self) -> str:
        """Interner Helper zum Lesen von DOCX mittels python-docx."""
        doc = docx.Document(self.current_file_path)
        # Absätze verbinden mit Newline
        return "\n".join([para.text for para in doc.paragraphs])