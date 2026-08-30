"""
config.py
---------
Un semplice contenitore di preferenze, salvato come config.json nella
radice di KClick, così lo stato dell'app resta dentro la cartella del
programma (nessun file sparso in giro per il sistema tipo ~/.config).

Uso tipico:
    cfg = Config.load()
    cfg.master_volume = 0.8
    cfg.save()
"""
from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

from .app_paths import CONFIG_FILE, SOUNDPACKS_DIR


@dataclass
class Config:
    enabled: bool = True          # stato on/off del suono (persiste tra i riavvii)
    soundpack: str = "default"    # nome sottocartella in soundpacks/
    master_volume: float = 0.7    # 0.0 - 1.0
    every_n: int = 2              # suona 1 battitura ogni N (skip-count)
    debounce_ms: int = 40         # intervallo minimo tra due suoni, in ms
    autostart: bool = False       # avvio automatico al login (backend del sistema operativo)

    @classmethod
    def load(cls) -> "Config":
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text())
                # Ignora eventuali chiavi sconosciute (es. da versioni future)
                known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
                return cls(**known)
            except (json.JSONDecodeError, TypeError):
                pass  # file corrotto: si riparte con i default
        return cls()

    def save(self) -> None:
        CONFIG_FILE.write_text(json.dumps(asdict(self), indent=2))

    def soundpack_path(self) -> Path:
        return SOUNDPACKS_DIR / self.soundpack

    @staticmethod
    def available_soundpacks() -> list[str]:
        if not SOUNDPACKS_DIR.exists():
            return []
        return sorted(p.name for p in SOUNDPACKS_DIR.iterdir() if p.is_dir())
