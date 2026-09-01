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

import os
import random
from pathlib import Path

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from .sound_categories import ALL_CATEGORIES


class AudioEngine:
    def __init__(self, master_volume: float = 0.7):
        # 44.1kHz, 16 bit, stereo, buffer piccolo per bassa latenza.
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=256,
        )
        pygame.mixer.init()

        # Più canali del default (8) per non restare "senza voci"
        # durante una scrittura molto veloce.
        pygame.mixer.set_num_channels(16)

        self.master_volume = master_volume
        self._sounds: dict[str, list[pygame.mixer.Sound]] = {}

        # Ultimo campione riprodotto per ciascuna categoria.
        # Serve a evitare due ripetizioni consecutive dello stesso WAV
        # quando la categoria dispone di più varianti.
        self._last_sound: dict[str, pygame.mixer.Sound] = {}

    def load_soundpack(self, pack_dir: Path) -> list[str]:
        """
        Carica tutte le categorie trovate in pack_dir.

        Ritorna la lista delle categorie per cui non è stato trovato
        alcun WAV. Il caricamento di un nuovo soundpack azzera anche
        la memoria dell'ultimo campione riprodotto.
        """
        self._sounds.clear()
        self._last_sound.clear()

        missing = []

        for category in ALL_CATEGORIES:
            cat_dir = pack_dir / category
            files = []

            if cat_dir.is_dir():
                files = sorted(cat_dir.glob("*.wav"))

            if not files:
                missing.append(category)
                continue

            self._sounds[category] = [
                pygame.mixer.Sound(str(path))
                for path in files
            ]

        return missing

    def set_master_volume(self, volume: float) -> None:
        self.master_volume = max(0.0, min(1.0, volume))

    def play(self, category: str) -> None:
        """
        Riproduce un suono casuale della categoria richiesta.

        Se la categoria non contiene suoni, usa "generic" come fallback.
        Quando esistono più varianti, lo stesso campione non può essere
        scelto due volte consecutivamente.
        """
        effective_category = category

        variants = self._sounds.get(effective_category)
        if not variants:
            effective_category = "generic"
            variants = self._sounds.get(effective_category)

        if not variants:
            return

        if len(variants) == 1:
            sound = variants[0]
        else:
            previous = self._last_sound.get(effective_category)
            choices = [
                sound
                for sound in variants
                if sound is not previous
            ]
            sound = random.choice(choices)

        self._last_sound[effective_category] = sound

        sound.set_volume(self.master_volume)
        sound.play()
