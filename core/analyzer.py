# -*- coding: utf-8 -*-
"""
Modul für die KI-gestützte Anforderungsanalyse.

Dieses Modul stellt die Klasse RequirementAnalyzer bereit, die als Wrapper
um das Ollama-Framework fungiert. Sie sendet Textdaten an ein lokales LLM
(Large Language Model) und erzwingt durch System-Prompts eine strukturierte
Ausgabe von funktionalen und nicht-funktionalen Anforderungen.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

import textwrap
import ollama


class RequirementAnalyzer:
    """
    Analysiert Texte auf Anforderungen mittels lokaler KI-Modelle.

    Diese Klasse konfiguriert den System-Prompt für den Requirements-Engineering-
    Kontext und handhabt die Kommunikation mit der Ollama-API.

    Attributes:
        model_name (str): Der Name des zu verwendenden Ollama-Modells 
                          (z. B. "qwen2.5:3b").
        max_input_length (int): Maximale Zeichenanzahl des Eingabetextes 
                                zur Vermeidung von Kontext-Überlauf.
    """

    # Standard-Limit für den Kontext (Tokens sparen & Abstürze vermeiden)
    MAX_INPUT_LENGTH = 12000

    def __init__(self, model_name: str = "qwen2.5:3b") -> None:
        """
        Initialisiert den Analyzer mit dem gewünschten Modell.

        Args:
            model_name (str): Bezeichner des Modells in Ollama.
        """
        self.model_name = model_name
        
        # Definition des System-Prompts mit textwrap für sauberen Code-Stil.
        # .strip() entfernt führende/nachfolgende Leerzeilen.
        self._system_prompt = textwrap.dedent("""
            Du bist ein Requirements Engineer Bot.
            
            REGELN:
            1. Antworte IMMER auf Deutsch.
            2. Keine Einleitungen oder Verabschiedungen ("Hier ist das Ergebnis...").
            3. Nutze NUR das folgende Markdown-Format für die Ausgabe:

            # Analyse-Bericht
            
            ## 1. Zusammenfassung
            [Eine kurze Zusammenfassung des Inhalts]

            ## 2. Funktionale Anforderungen
            - [REQ-F-01] [Anforderungstext]
            - [REQ-F-02] [Anforderungstext]

            ## 3. Nicht-Funktionale Anforderungen
            - [REQ-N-01] [Anforderungstext]

            ## 4. Offene Fragen / Risiken
            - [Text]
        """).strip()

    def analyze_text(self, text_input: str) -> str:
        """
        Sendet den Text an das LLM und gibt die strukturierte Analyse zurück.

        Der Eingabetext wird automatisch auf `MAX_INPUT_LENGTH` gekürzt,
        um die Token-Limits des Modells nicht zu sprengen.

        Args:
            text_input (str): Der rohe Text aus dem Dokument.

        Returns:
            str: Der generierte Analysebericht im Markdown-Format oder
                 eine Fehlermeldung, die mit "Fehler:" beginnt.
        """
        try:
            # Eingabe kürzen, um Kontext-Fenster nicht zu überladen
            truncated_input = text_input[:self.MAX_INPUT_LENGTH]

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system', 
                        'content': self._system_prompt
                    },
                    {
                        'role': 'user', 
                        'content': f"Input Text:\n\n{truncated_input}"
                    }
                ]
            )

            # Extrahiere den Inhalt der Antwort
            content = response.get('message', {}).get('content', '')
            
            if not content:
                return "Fehler: Leere Antwort vom Modell erhalten."
                
            return content

        except Exception as e:
            # Fehlerformat passend zur GUI-Logik (MainWindow prüft auf "Fehler")
            return f"Fehler: {str(e)}"