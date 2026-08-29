"""
gui/tray.py
-----------
Icona nel pannello di sistema (system tray). Disegniamo noi stessi
due semplici icone (pallino verde/grigio) con QPainter, così non
serve nessun file immagine esterno da distribuire col progetto.

Click sinistro  -> toggle on/off
Click destro    -> menu contestuale (Impostazioni / Esci)
"""
from __future__ import annotations
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication


def _make_dot_icon(color: QColor) -> QIcon:
    size = QSize(64, 64)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(color)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(8, 8, 48, 48)
    painter.end()
    return QIcon(pixmap)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, config, audio_engine, open_settings_callback, parent=None):
        self._icon_on = _make_dot_icon(QColor("#2ecc71"))   # verde
        self._icon_off = _make_dot_icon(QColor("#7f8c8d"))  # grigio
        super().__init__(self._icon_on if config.enabled else self._icon_off, parent)

        self.config = config
        self.audio = audio_engine
        self.open_settings_callback = open_settings_callback

        self.setToolTip("KClick")
        self._build_menu()
        self.activated.connect(self._on_activated)
        self._refresh_icon()

    def _build_menu(self) -> None:
        menu = QMenu()
        self._toggle_action = QAction("Disattiva" if self.config.enabled else "Attiva", self)
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

    def toggle(self) -> None:
        self.config.enabled = not self.config.enabled
        self.config.save()
        self._refresh_icon()

    def _refresh_icon(self) -> None:
        self.setIcon(self._icon_on if self.config.enabled else self._icon_off)
        self._toggle_action.setText("Disattiva" if self.config.enabled else "Attiva")
        self.setToolTip("KClick — attivo" if self.config.enabled else "KClick — in pausa")
