"""
autostart.py
------------
Installa/disinstalla il servizio systemd --user che avvia
KClick automaticamente al login. Scriviamo il file .service
puntando all'interprete Python DENTRO il virtualenv, così il
servizio funziona anche se in futuro sposti o rinomini il progetto
(basta rigenerare il file).
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

from core.app_paths import APP_ROOT

SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"
SERVICE_NAME = "kclick.service"
SERVICE_PATH = SYSTEMD_USER_DIR / SERVICE_NAME



def _service_content() -> str:
    python_bin = sys.executable  # es. /percorso/KClick/.venv/bin/python
    entrypoint = APP_ROOT / "kclick.py"
    return f"""[Unit]
Description=KClick - suoni da macchina da scrivere
After=graphical-session.target
PartOf=graphical-session.target

[Service]
Type=simple
ExecStart={python_bin} {entrypoint}
Restart=on-failure
RestartSec=3

[Install]
WantedBy=graphical-session.target
"""


def install_and_enable() -> None:
    SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)
    SERVICE_PATH.write_text(_service_content())
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    subprocess.run(["systemctl", "--user", "enable", SERVICE_NAME], check=False)


def disable_and_remove() -> None:
    if SERVICE_PATH.exists():
        subprocess.run(
            ["systemctl", "--user", "disable", SERVICE_NAME],
            check=False,
        )
        SERVICE_PATH.unlink()

    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)


def set_autostart(enabled: bool) -> None:
    if enabled:
        install_and_enable()
    else:
        disable_and_remove()
