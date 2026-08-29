"""
audio_engine.py
----------------
Carica in RAM tutti i file audio di un soundpack (una volta sola,
all'avvio) e li riproduce a comando. Usiamo pygame.mixer perché
gestisce da solo più "canali" simultanei: se due suoni si accavallano
(scrittura veloce) NON si tagliano a vicenda, vengono mixati.

Perché precaricare: leggere un file da disco ad ogni pressione tasto
introduce una latenza percepibile. Meglio pagare il costo una volta
sola all'avvio.
"""
from __future__ import annotations
import random
from pathlib import Path

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from .sound_categories import ALL_CATEGORIES


class AudioEngine:
    def __init__(self, master_volume: float = 0.7):
        # 44.1kHz, 16 bit, stereo, buffer piccolo per bassa latenza.
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)
        pygame.mixer.init()
        # Più canali del default (8) per non restare "senza voci"
        # durante una scrittura molto veloce.
        pygame.mixer.set_num_channels(16)

        self.master_volume = master_volume
        self._sounds: dict[str, list[pygame.mixer.Sound]] = {}

    def load_soundpack(self, pack_dir: Path) -> list[str]:
        """
        Carica tutte le categorie trovate in pack_dir. Ritorna la lista
        di categorie per cui NON è stato trovato nessun file (utile
        per avvisare l'utente in GUI, senza far crashare il programma).
        """
        self._sounds.clear()
        missing = []
        for category in ALL_CATEGORIES:
            cat_dir = pack_dir / category
            files = []
            if cat_dir.is_dir():
                files = sorted(cat_dir.glob("*.wav"))
            if not files:
                missing.append(category)
                continue
            self._sounds[category] = [pygame.mixer.Sound(str(f)) for f in files]
        return missing

    def set_master_volume(self, volume: float) -> None:
        self.master_volume = max(0.0, min(1.0, volume))

    def play(self, category: str) -> None:
        """Riproduce un suono a caso tra le varianti disponibili per
        quella categoria. Se la categoria non ha suoni caricati (o non
        esiste), fa "fallback" sulla categoria 'generic' se disponibile,
        altrimenti non fa nulla (nessun crash)."""
        variants = self._sounds.get(category)
        if not variants:
            variants = self._sounds.get("generic")
        if not variants:
            return
        sound = random.choice(variants)
        sound.set_volume(self.master_volume)
        sound.play()  # pygame trova da solo un canale libero
