"""
app_paths.py
------------
Percorsi condivisi di KClick.

La radice dell'app viene determinata una volta sola:
- da sorgenti: cartella che contiene kclick.py;
- build PyInstaller frozen: cartella che contiene KClick.exe.

Tutti gli altri percorsi dell'app vengono derivati da questa radice.
"""
from __future__ import annotations

import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    APP_ROOT = Path(sys.executable).resolve().parent
else:
    APP_ROOT = Path(__file__).resolve().parent.parent

CONFIG_FILE = APP_ROOT / "config.json"

SOUNDPACKS_DIR = APP_ROOT / "soundpacks"
ICONS_DIR = APP_ROOT / "gui" / "icons"
LAUNCHER_ICON = ICONS_DIR / "launcher" / "kclick-icon-launcher.svg"
TRAY_ICONS_DIR = ICONS_DIR / "tray"
