#!/usr/bin/env python3
"""
kclick.py
---------
Punto di ingresso. Ordine di avvio importante:
1. Config (preferenze da disco)
2. AudioEngine (precarica i suoni PRIMA di iniziare ad ascoltare)
3. InputBackend + InputController (thread separato, parte per ultimo)
4. GUI (tray + finestra impostazioni, gira nel thread principale)
"""
import sys

# KClick non scrive cache Python su disco: la cartella del programma
# e la home dell'utente restano libere da __pycache__ e file .pyc.
# Questa impostazione deve precedere gli import dei moduli dell'app.
sys.dont_write_bytecode = True

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

from core.app_paths import LAUNCHER_ICON
from core.config import Config
from core.audio_engine import AudioEngine
from core.input_controller import InputController
from backends import InputBackend, set_autostart
from gui.tray import TrayIcon
from gui.main_window import SettingsWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # la finestra impostazioni si chiude, l'app resta nel tray

    app_icon_path = LAUNCHER_ICON
    app_icon = QIcon(str(app_icon_path))
    if app_icon.isNull():
        print(f"[KClick] Icona applicazione non trovata o non valida: {app_icon_path}")
    else:
        app.setWindowIcon(app_icon)

    cfg = Config.load()
    cfg.save()  # crea subito config.json anche al primissimo avvio, con i valori di default

    audio = AudioEngine(master_volume=cfg.master_volume)
    missing = audio.load_soundpack(cfg.soundpack_path())
    if missing:
        print(f"[KClick] Categorie senza suoni nel pack '{cfg.soundpack}': {missing}")
        print("              (verranno riprodotti suoni 'generic' al loro posto, se presenti)")

    # Manteniamo il meccanismo di autostart del sistema operativo
    # coerente con la preferenza salvata in config.json.
    set_autostart(cfg.autostart)

    def _on_input_error(message: str) -> None:
        # I popup di Qt vanno mostrati dal thread principale: usiamo
        # QTimer.singleShot(0, ...) per "rimbalzare" la chiamata lì,
        # dato che questa callback arriva dal thread di input.
        QTimer.singleShot(0, lambda: QMessageBox.warning(None, "KClick", message))

    input_backend = InputBackend()
    input_controller = InputController(
        config=cfg,
        audio_engine=audio,
        input_backend=input_backend,
        on_error=_on_input_error,
    )
    input_controller.start()

    settings_window: SettingsWindow | None = None

    def open_settings() -> None:
        nonlocal settings_window
        if settings_window is None:
            settings_window = SettingsWindow(cfg, audio, autostart_callback=set_autostart)
        settings_window.show()
        settings_window.raise_()
        settings_window.activateWindow()

    tray = TrayIcon(cfg, audio, open_settings_callback=open_settings)
    tray.show()

    exit_code = app.exec()
    input_controller.stop()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
