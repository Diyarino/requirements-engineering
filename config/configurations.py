# -*- coding: utf-8 -*-
"""
Zentrale Konfigurationsdatei der Anwendung.

In diesem Modul werden alle statischen Konstanten, UI-Parameter und
Design-Einstellungen verwaltet. Dies ermöglicht eine einfache Anpassung
des Look & Feel, ohne den Quellcode der Logik-Module ändern zu müssen.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

from typing import List, Tuple

# -----------------------------------------------------------------------------
# 1. Allgemeine Anwendungseinstellungen
# -----------------------------------------------------------------------------
APP_TITLE: str = "AI Requirements Engineer Pro"
APP_SIZE: str = "700x500"

# -----------------------------------------------------------------------------
# 2. Design & Themes (CustomTkinter)
# -----------------------------------------------------------------------------
# Optionen: "System" (folgt OS), "Dark", "Light"
APPEARANCE_MODE: str = "Dark"

# Optionen: "blue" (Standard), "green", "dark-blue"
COLOR_THEME: str = "blue"

# -----------------------------------------------------------------------------
# 3. Farbpalette (Hex-Codes)
# -----------------------------------------------------------------------------
# Primärfarben für Interaktionselemente
COLOR_BTN_SELECT: str = "#3B8ED0"  # Standard Blau
COLOR_BTN_ACTION: str = "#2CC985"  # Bestätigungs-Grün
COLOR_BTN_HOVER: str  = "#208f61"  # Dunkleres Grün für Hover-Effekt

# Status-Farben (für Feedback-Meldungen im UI)
COLOR_ERROR: str   = "#FF5555"     # Rot
COLOR_SUCCESS: str = "#2CC985"     # Grün
COLOR_WARNING: str = "#E0A800"     # Gelb/Orange

# -----------------------------------------------------------------------------
# 4. Dateiverwaltung
# -----------------------------------------------------------------------------
# Filter für den Datei-Auswahl-Dialog.
# Hinweis: *.doc wurde entfernt, da python-docx nur XML-basierte *.docx unterstützt.
ALLOWED_FILETYPES: List[Tuple[str, str]] = [
    ("Unterstützte Dokumente", "*.pdf *.docx"),
    ("PDF Dateien", "*.pdf"),
    ("Word Dateien", "*.docx")
]