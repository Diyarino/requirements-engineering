# -*- coding: utf-8 -*-
"""
Paket-Initialisierung für Anwendungskonfigurationen.

Dieses Modul markiert das Verzeichnis `config` als Python-Paket und
exponiert die globalen Konstanten aus `configurations.py`, sodass sie
direkt über den Paket-Namespace importiert werden können.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

# Importiert alle Konstanten aus configurations.py in den Paket-Namespace.
# Dies ermöglicht den Zugriff via:
#   import config
#   print(config.APP_TITLE)
# anstelle von:
#   from config import configurations
#   print(configurations.APP_TITLE)
from .configurations import *