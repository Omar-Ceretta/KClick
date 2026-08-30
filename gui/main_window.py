"""
gui/main_window.py
-------------------
Finestra di impostazioni, minimale ma completa. Le modifiche si
applicano "live" (InputController e AudioEngine leggono self.config
in tempo reale), il pulsante Salva serve solo a rendere le
preferenze persistenti su disco.
"""
from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QSlider, QLabel,
    QCheckBox, QDialogButtonBox, QHBoxLayout, QWidget
)
from PySide6.QtCore import Qt

from core import config as config_module


class SettingsWindow(QDialog):
    def __init__(self, config, audio_engine, autostart_callback, parent=None):
        super().__init__(parent)
        self.config = config
        self.audio = audio_engine
        self.autostart_callback = autostart_callback  # funzione(bool) -> backend autostart della piattaforma

        self.setWindowTitle("KClick — Impostazioni")
        self.setMinimumWidth(360)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # --- Soundpack ---
        self.soundpack_combo = QComboBox()
        self.soundpack_combo.addItems(config_module.Config.available_soundpacks())
        self.soundpack_combo.currentTextChanged.connect(self._on_soundpack_changed)
        form.addRow("Soundpack:", self.soundpack_combo)

        # --- Volume ---
        self.volume_slider, volume_row = self._make_slider(0, 100, self._on_volume_changed)
        form.addRow("Volume:", volume_row)

        # --- Skip-count ("ogni tot battiture") ---
        self.every_n_slider, every_n_row = self._make_slider(1, 5, self._on_every_n_changed)
        form.addRow("Suona 1 battuta ogni:", every_n_row)

        # --- Debounce ---
        self.debounce_slider, debounce_row = self._make_slider(0, 200, self._on_debounce_changed)
        form.addRow("Intervallo minimo (ms):", debounce_row)

        layout.addLayout(form)

        # --- Autostart ---
        self.autostart_check = QCheckBox("Avvia automaticamente al login")
        self.autostart_check.stateChanged.connect(self._on_autostart_changed)
        layout.addWidget(self.autostart_check)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.close)
        buttons.accepted.connect(self.close)
        layout.addWidget(buttons)

    @staticmethod
    def _make_slider(minimum: int, maximum: int, on_change) -> tuple[QSlider, QWidget]:
        """Crea uno slider con un'etichetta numerica accanto che si
        aggiorna in tempo reale mentre si trascina."""
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(minimum, maximum)
        value_label = QLabel(str(minimum))
        value_label.setFixedWidth(36)

        def _handler(value: int) -> None:
            value_label.setText(str(value))
            on_change(value)

        slider.valueChanged.connect(_handler)
        row_layout.addWidget(slider)
        row_layout.addWidget(value_label)
        return slider, row

    def _load_values(self) -> None:
        self.soundpack_combo.setCurrentText(self.config.soundpack)
        self.volume_slider.setValue(int(self.config.master_volume * 100))
        self.every_n_slider.setValue(self.config.every_n)
        self.debounce_slider.setValue(self.config.debounce_ms)
        self.autostart_check.setChecked(self.config.autostart)

    # --- Handler: ognuno aggiorna config, il motore live, e salva su disco ---

    def _on_soundpack_changed(self, name: str) -> None:
        if not name:
            return
        self.config.soundpack = name
        missing = self.audio.load_soundpack(self.config.soundpack_path())
        if missing:
            print(f"[KClick] Attenzione: categorie senza suoni nel pack '{name}': {missing}")
        self.config.save()

    def _on_volume_changed(self, value: int) -> None:
        self.config.master_volume = value / 100
        self.audio.set_master_volume(self.config.master_volume)
        self.config.save()

    def _on_every_n_changed(self, value: int) -> None:
        self.config.every_n = value
        self.config.save()

    def _on_debounce_changed(self, value: int) -> None:
        self.config.debounce_ms = value
        self.config.save()

    def _on_autostart_changed(self, state: int) -> None:
        enabled = state != 0  # 0 = Unchecked, qualsiasi altro valore = checked
        self.config.autostart = enabled
        self.config.save()
        self.autostart_callback(enabled)
