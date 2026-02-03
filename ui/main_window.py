# -*- coding: utf-8 -*-
"""
Hauptfenster der Anwendung (GUI-Layer).

Dieses Modul definiert die Klasse MainWindow, die als zentrale Benutzeroberfläche
fungiert. Es verknüpft die Benutzerinteraktionen mit der Geschäftslogik
(FileHandler, Analyzer, Exporter) und steuert den Ablauf der Analyse
in einem separaten Thread, um das Einfrieren der Oberfläche zu verhindern.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

import threading
from typing import Optional
from tkinter import filedialog, messagebox

import customtkinter as ctk

# Lokale Module
from config import configurations
from core.file_handler import FileHandler
from core.analyzer import RequirementAnalyzer
from core.exporter import ReportExporter
from ui.result_window import ResultWindow


class MainWindow(ctk.CTk):
    """
    Die Hauptklasse der grafischen Benutzeroberfläche.

    Erbt von customtkinter.CTk und stellt die primäre Schnittstelle für den
    Benutzer dar. Sie verwaltet den Dateiauswahldialog, den Fortschrittsbalken
    und delegiert die eigentliche Arbeit an Worker-Threads.

    Attributes:
        file_handler (FileHandler): Verwaltet Datei-Leseoperationen.
        analyzer (RequirementAnalyzer): Führt die KI-Analyse durch.
        exporter (ReportExporter): Generiert PDF/DOCX-Berichte.
    """

    def __init__(self) -> None:
        """Initialisiert das Hauptfenster, die Logik-Module und das UI-Layout."""
        super().__init__()

        # Initialisierung der Geschäftslogik
        self.file_handler = FileHandler()
        # TODO: Modellname idealerweise auch in configurations auslagern
        self.analyzer = RequirementAnalyzer(model_name="qwen2.5:3b")
        self.exporter = ReportExporter()

        # Grundlegende Fensterkonfiguration
        self.title(configurations.APP_TITLE)
        self.geometry(configurations.APP_SIZE)
        
        ctk.set_appearance_mode(configurations.APPEARANCE_MODE)
        ctk.set_default_color_theme(configurations.COLOR_THEME)

        # Aufbau der GUI-Elemente
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Erstellt und platziert alle Widgets im Grid-Layout.
        """
        # Grid-Konfiguration für responsive Anpassung
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # 1. Titel
        self.lbl_title = ctk.CTkLabel(
            self, 
            text="AI Requirements Engineer", 
            font=("Roboto", 24, "bold")
        )
        self.lbl_title.grid(row=0, column=0, pady=20)

        # 2. Dateiname Anzeige
        self.lbl_filename = ctk.CTkLabel(self, text="Keine Datei ausgewählt")
        self.lbl_filename.grid(row=1, column=0)

        # 3. Button: Datei wählen
        self.btn_select = ctk.CTkButton(
            self, 
            text="Datei wählen", 
            command=self.on_select_file
        )
        self.btn_select.grid(row=2, column=0)

        # 4. Button: Analyse starten
        self.btn_run = ctk.CTkButton(
            self, 
            text="Analyse starten", 
            command=self.on_start_processing, 
            state="disabled"
        )
        self.btn_run.grid(row=3, column=0)

        # 5. Ladebalken (initial ausgeblendet)
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress_bar.grid(row=4, column=0)
        self.progress_bar.grid_remove()

        # 6. Status-Label
        self.lbl_status = ctk.CTkLabel(self, text="")
        self.lbl_status.grid(row=5, column=0, pady=20)

    # -------------------------------------------------------------------------
    # UI Interaktions-Methoden
    # -------------------------------------------------------------------------

    def on_select_file(self) -> None:
        """
        Öffnet einen Dateidialog und aktualisiert den FileHandler.

        Wenn eine Datei erfolgreich ausgewählt wurde, wird der 'Start'-Button
        aktiviert und der Dateiname in der GUI angezeigt.
        """
        path = filedialog.askopenfilename(
            filetypes=configurations.ALLOWED_FILETYPES
        )
        
        if path:
            if self.file_handler.set_file_path(path):
                filename = self.file_handler.get_filename()
                self.lbl_filename.configure(text=f"Datei: {filename}")
                self.btn_run.configure(state="normal")
                self.lbl_status.configure(text="Bereit.")

    def on_start_processing(self) -> None:
        """
        Bereitet die UI auf den Analyseprozess vor und startet den Worker-Thread.

        Deaktiviert Buttons, um Mehrfachklicks zu verhindern, und startet
        die Ladeanimation.
        """
        # UI sperren
        self.btn_run.configure(state="disabled")
        self.btn_select.configure(state="disabled")
        
        # Animation starten
        self.progress_bar.grid()
        self.progress_bar.start()
        
        # Hintergrundprozess starten (Threading verhindert GUI-Freeze)
        threading.Thread(target=self._background_task, daemon=True).start()

    def update_status(self, text: str, color: str = "white") -> None:
        """
        Aktualisiert das Status-Label Thread-sicher.

        Args:
            text: Der anzuzeigende Text.
            color: Die Textfarbe (Hex-Code oder Name).
        """
        self.after(0, lambda: self.lbl_status.configure(
            text=text, 
            text_color=color
        ))

    # -------------------------------------------------------------------------
    # Hintergrund-Logik (Worker Thread)
    # -------------------------------------------------------------------------

    def _background_task(self) -> None:
        """
        Führt die gesamte Verarbeitungs-Pipeline im Hintergrund aus.

        Ablauf:
        1. Text lesen
        2. Text bereinigen
        3. KI-Analyse durchführen
        4. Ergebnisse exportieren (DOCX/PDF)
        5. Abschluss-Callback aufrufen
        """
        try:
            # Schritt 1: Datei einlesen
            self.update_status("Lese Datei...")
            raw_text = self.file_handler.read_text()
            
            # Einfache Fehlerprüfung basierend auf Rückgabewert
            if raw_text.startswith("Fehler"):
                self.after(0, lambda: self._finished_process(error=raw_text))
                return

            # Schritt 2: Preprocessing
            self.update_status("Bereinige Text...")
            clean_text = self.file_handler.preprocess_text()

            # Schritt 3: Analyse
            self.update_status("KI analysiert (bitte warten)...", "#3B8ED0")
            result_text = self.analyzer.analyze_text(clean_text)

            # Schritt 4: Export
            self.update_status("Erstelle Dokument...", "#E0A800")  # Gelb
            current_file_path = self.file_handler.get_full_path()
            
            # Exportiert Bericht und gibt Pfade zurück
            path_docx, path_pdf = self.exporter.save_reports(
                result_text, 
                current_file_path
            )

            # Schritt 5: Abschluss
            self.after(0, lambda: self._finished_process(
                result=result_text, 
                doc=path_docx, 
                pdf=path_pdf
            ))

        except Exception as e:
            # Fängt unerwartete Abstürze ab
            error_msg = f"Kritischer Fehler: {str(e)}"
            self.after(0, lambda: self._finished_process(error=error_msg))

    def _finished_process(
        self, 
        result: Optional[str] = None, 
        doc: Optional[str] = None, 
        pdf: Optional[str] = None, 
        error: Optional[str] = None
    ) -> None:
        """
        Callback, der nach Abschluss des Threads im Haupt-Thread ausgeführt wird.

        Stoppt die Animation, reaktiviert Buttons und zeigt das Ergebnis
        oder eine Fehlermeldung an.

        Args:
            result: Der generierte Analyse-Text.
            doc: Pfad zur DOCX-Datei.
            pdf: Pfad zur PDF-Datei.
            error: Fehlermeldung, falls etwas schiefging.
        """
        # UI zurücksetzen
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.btn_run.configure(state="normal", text="Neu starten")
        self.btn_select.configure(state="normal")

        if error:
            self.lbl_status.configure(text="Fehler!", text_color="#FF5555")
            messagebox.showerror("Fehler", error)
        else:
            self.lbl_status.configure(
                text="✔ Fertig gespeichert.", 
                text_color="#2CC985"
            )
            
            # Ergebnisfenster öffnen (sofern Ergebnis vorhanden)
            if result and doc:
                ResultWindow(self, result, doc, pdf)