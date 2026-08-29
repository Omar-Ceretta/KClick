"""
autostart.py
------------
Autostart di KClick su Windows tramite la chiave Run dell'utente.

Nel Registro resta soltanto il comando necessario ad avviare KClick;
configurazione, soundpack e dati continuano a vivere nella cartella
del programma.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import winreg

APP_NAME = "KClick"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

PROJECT_DIR = Path(__file__).resolve().parents[2]


def _launch_command() -> str:
    """Restituisce il comando da registrare per l'avvio di KClick."""
    if getattr(sys, "frozen", False):
        # Build impacchettata: sys.executable è KClick.exe.
        return subprocess.list2cmdline([sys.executable])

    # Esecuzione da sorgenti: preferiamo pythonw.exe, se disponibile,
    # per non aprire una finestra console all'accesso a Windows.
    python_bin = Path(sys.executable)
    if python_bin.name.lower() == "python.exe":
        pythonw = python_bin.with_name("pythonw.exe")
        if pythonw.exists():
            python_bin = pythonw

    entrypoint = PROJECT_DIR / "kclick.py"
    return subprocess.list2cmdline([str(python_bin), str(entrypoint)])


def install_and_enable() -> None:
    """Crea o aggiorna il riferimento di KClick nell'autostart utente."""
    with winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER,
        RUN_KEY,
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        winreg.SetValueEx(
            key,
            APP_NAME,
            0,
            winreg.REG_SZ,
            _launch_command(),
        )


def disable_and_remove() -> None:
    """Rimuove il riferimento di KClick, se presente."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            RUN_KEY,
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
    except FileNotFoundError:
        pass


def set_autostart(enabled: bool) -> None:
    if enabled:
        install_and_enable()
    else:
        disable_and_remove()
