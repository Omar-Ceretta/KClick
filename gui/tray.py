"""
gui/tray.py
-----------
Icona nel pannello di sistema (system tray).

Lo stato di KClick viene comunicato dalla forma dell'icona, non dal colore:
- attivo: icona KClick normale;
- in pausa: stessa icona con segno di cancellazione.

Sono previste varianti dedicate per pannelli chiari e scuri.

Click sinistro  -> toggle on/off
Click destro    -> menu contestuale (Impostazioni / Esci)
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QPalette
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from core.app_paths import TRAY_ICONS_DIR


def _is_dark_theme() -> bool:
    """Restituisce True se il tema applicativo corrente è scuro."""
    app = QApplication.instance()
    if app is None:
        return False

    scheme = app.styleHints().colorScheme()

    if scheme == Qt.ColorScheme.Dark:
        return True
    if scheme == Qt.ColorScheme.Light:
        return False

    # Fallback per piattaforme che restituiscono ColorScheme.Unknown.
    window_color = app.palette().color(QPalette.Window)
    return window_color.lightness() < 128


def _tray_icon(enabled: bool) -> QIcon:
    """Carica l'icona tray adatta a stato e tema correnti."""
    state = "on" if enabled else "off"
    theme = "dark" if _is_dark_theme() else "light"
    path = TRAY_ICONS_DIR / f"kclick-tray-{state}-{theme}.png"
    return QIcon(str(path))


class TrayIcon(QSystemTrayIcon):
    def __init__(self, config, audio_engine, open_settings_callback, parent=None):
        super().__init__(_tray_icon(config.enabled), parent)

        self.config = config
        self.audio = audio_engine
        self.open_settings_callback = open_settings_callback

        self.setToolTip("KClick")
        self._build_menu()
        self.activated.connect(self._on_activated)

        app = QApplication.instance()
        if app is not None:
            app.styleHints().colorSchemeChanged.connect(
                self._on_color_scheme_changed
            )

        self._refresh_icon()

    def _build_menu(self) -> None:
        menu = QMenu()
        self._toggle_action = QAction(
            "Disattiva" if self.config.enabled else "Attiva",
            self,
        )
        self._toggle_action.triggered.connect(self.toggle)
        menu.addAction(self._toggle_action)

        settings_action = QAction("Impostazioni...", self)
        settings_action.triggered.connect(self.open_settings_callback)
        menu.addAction(settings_action)

        menu.addSeparator()
        quit_action = QAction("Esci", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def _on_activated(self, reason) -> None:
        # Trigger = click sinistro. Il click destro apre già il
        # context menu da solo (comportamento nativo di Qt).
        if reason == QSystemTrayIcon.Trigger:
            self.toggle()

    def _on_color_scheme_changed(self, _scheme) -> None:
        self._refresh_icon()

    def toggle(self) -> None:
        self.config.enabled = not self.config.enabled
        self.config.save()
        self._refresh_icon()

    def _refresh_icon(self) -> None:
        self.setIcon(_tray_icon(self.config.enabled))
        self._toggle_action.setText(
            "Disattiva" if self.config.enabled else "Attiva"
        )
        self.setToolTip(
            "KClick — attivo" if self.config.enabled else "KClick — in pausa"
        )
