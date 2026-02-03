# -*- coding: utf-8 -*-
"""
Haupt-Einstiegspunkt der Anwendung.

Dieses Modul dient als Startpunkt für die Software. Es initialisiert
die grafische Benutzeroberfläche (GUI) und startet den Event-Loop.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

from ui.main_window import MainWindow


def main() -> None:
    """
    Initialisiert die Anwendung und startet die Hauptschleife.

    Diese Funktion instanziiert die :class:`MainWindow`-Klasse und ruft deren
    `mainloop`-Methode auf, um die GUI am Leben zu erhalten, bis der Benutzer
    das Fenster schließt.

    Returns:
        None
    """
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()