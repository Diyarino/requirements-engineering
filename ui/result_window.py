# -*- coding: utf-8 -*-
"""
Modul für das Ergebnisfenster der Analyse.

Dieses Modul stellt die Klasse ResultWindow bereit, die als modales
Dialogfenster dient, um die generierten Analyseberichte und Speicherpfade
anzuzeigen.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

from typing import Optional, Any
import customtkinter as ctk


class ResultWindow(ctk.CTkToplevel):
    """
    Ein Pop-up-Fenster zur Anzeige der Analyseergebnisse.

    Dieses Fenster zeigt den vollständigen Text des Berichts in einem
    scrollbaren Textfeld an und informiert den Benutzer über die Speicherorte
    der generierten Dateien (DOCX/PDF).

    Attributes:
        parent (Any): Das übergeordnete Fenster (meist MainWindow).
        result_text (str): Der anzuzeigende Berichtstext.
        path_docx (str): Der Dateipfad der erstellten Word-Datei.
        path_pdf (Optional[str]): Der Dateipfad der erstellten PDF-Datei (optional).
    """

    def __init__(
        self,
        parent: Any,
        result_text: str,
        path_docx: str,
        path_pdf: Optional[str] = None
    ) -> None:
        """
        Initialisiert das Ergebnisfenster und baut das UI-Layout auf.

        Args:
            parent: Das Eltern-Widget (für die Positionierung).
            result_text: Der Inhalt der Analyse.
            path_docx: Absoluter oder relativer Pfad zur DOCX-Datei.
            path_pdf: Absoluter oder relativer Pfad zur PDF-Datei (oder None).
        """
        super().__init__(parent)

        # Fenstereinstellungen
        self.title("Analyse Ergebnis")
        self.geometry("800x600")

        # Grid-Layout Konfiguration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Textfeld soll vertikal wachsen

        # Fokus-Hack: Fenster kurz in den Vordergrund zwingen, damit es nicht
        # hinter dem Hauptfenster verschwindet (typisches Tkinter/CTK Verhalten).
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        # ---------------------------------------------------------
        # 1. Header
        # ---------------------------------------------------------
        self.lbl_header = ctk.CTkLabel(
            self,
            text="Fertiger Analyse-Bericht",
            font=("Roboto", 20, "bold")
        )
        self.lbl_header.grid(row=0, column=0, pady=(20, 10))

        # ---------------------------------------------------------
        # 2. Textfeld (Ergebnis)
        # ---------------------------------------------------------
        self.textbox = ctk.CTkTextbox(
            self,
            font=("Consolas", 14),
            wrap="word"  # Automatischer Zeilenumbruch
        )
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Text einfügen und danach sperren (Read-Only)
        self.textbox.insert("0.0", result_text)
        self.textbox.configure(state="disabled")

        # ---------------------------------------------------------
        # 3. Info-Bereich (Dateipfade)
        # ---------------------------------------------------------
        # Dynamischer Aufbau des Info-Strings
        info_lines = ["✔ Gespeichert als:", f"📄 {path_docx}"]
        
        if path_pdf:
            info_lines.append(f"📄 {path_pdf}")
            
        info_text = "\n".join(info_lines)

        self.lbl_paths = ctk.CTkLabel(
            self,
            text=info_text,
            fg_color="#333333",  # Dunkler Hintergrund für Kontrast
            corner_radius=8,
            pady=10,
            padx=10,
            justify="left",
            font=("Roboto", 12)
        )
        self.lbl_paths.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # ---------------------------------------------------------
        # 4. Footer (Buttons)
        # ---------------------------------------------------------
        self.btn_close = ctk.CTkButton(
            self,
            text="Schließen",
            command=self.destroy,
            fg_color="#FF5555",
            hover_color="#cc0000"
        )
        self.btn_close.grid(row=3, column=0, pady=20)