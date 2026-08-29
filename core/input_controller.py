"""
input_controller.py
-------------------
Gestisce la logica comune degli eventi di tastiera di KClick.

Il backend specifico del sistema operativo rileva i tasti premuti
e li traduce in categorie sonore ("generic", "space", "enter"...).

InputController applica invece la logica indipendente dalla
piattaforma: attivazione, skip-count, debounce e riproduzione audio.

Lo skip-count (every_n) e il debounce si applicano soltanto ai tasti
generici. Le categorie speciali (spazio, Invio, Backspace ecc.)
suonano sempre quando KClick è attivo e non alterano il conteggio
dei tasti generici.
"""

from __future__ import annotations

import threading
import time


class InputController(threading.Thread):
    """
    Coordina il backend di input e il motore audio.

    I parametri live (enabled, every_n, debounce_ms) vengono letti
    direttamente dall'oggetto Config condiviso, così le modifiche
    effettuate dalla GUI hanno effetto immediato.
    """

    def __init__(self, config, audio_engine, input_backend, on_error=None):
        super().__init__(daemon=True)
        self.config = config
        self.audio = audio_engine
        self.input_backend = input_backend
        self.on_error = on_error

        self._stop_event = threading.Event()
        self._keystroke_count = 0
        self._last_play_ts = 0.0

    def stop(self) -> None:
        self._stop_event.set()

    def _should_play_generic(self) -> bool:
        """
        Applica skip-count e debounce a un keypress generico.

        Le categorie speciali non passano da qui: suonano sempre e
        non modificano né il conteggio né il timestamp del debounce.
        """
        self._keystroke_count += 1

        if self._keystroke_count % max(1, self.config.every_n) != 0:
            return False

        now = time.monotonic()

        if (now - self._last_play_ts) * 1000 < self.config.debounce_ms:
            return False

        self._last_play_ts = now
        return True

    def _handle_keypress(self, category: str) -> None:
        """Gestisce una categoria sonora ricevuta dal backend."""
        if not self.config.enabled:
            return

        if category != "generic":
            self.audio.play(category)
            return

        if self._should_play_generic():
            self.audio.play(category)

    def run(self) -> None:
        """Avvia il backend e riceve da esso le categorie dei keypress."""
        self.input_backend.run(
            stop_event=self._stop_event,
            on_keypress=self._handle_keypress,
            on_error=self.on_error,
        )
