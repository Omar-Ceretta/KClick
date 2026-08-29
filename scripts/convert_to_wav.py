#!/usr/bin/env python3
"""
scripts/convert_to_wav.py
--------------------------
Converte in .wav tutti i file audio (.mp3, .ogg) trovati in una
cartella sorgente, e li copia dentro una categoria del soundpack.

Usiamo ffmpeg via subprocess invece di una libreria Python, perché
è lo standard più affidabile per queste conversioni ed è quasi
certamente già installato (RPM Fusion, che probabilmente hai già
abilitato per i driver NVIDIA).

Esempio d'uso:
    python scripts/convert_to_wav.py ~/Scaricati/mechvibes_pack/keydown \\
        ../soundpacks/default/generic

    python scripts/convert_to_wav.py ~/miei_suoni/spazio.mp3 \\
        ../soundpacks/default/space
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

SUPPORTED_EXT = {".mp3", ".ogg", ".flac", ".m4a"}


def convert_one(src: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / (src.stem + ".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-ar", "44100", "-ac", "2", str(dest)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"  {src.name} -> {dest}")


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    source = Path(sys.argv[1]).expanduser()
    dest_dir = Path(sys.argv[2]).expanduser()

    if source.is_dir():
        files = [f for f in source.iterdir() if f.suffix.lower() in SUPPORTED_EXT]
        if not files:
            print(f"Nessun file audio supportato trovato in {source}")
            sys.exit(1)
        print(f"Conversione di {len(files)} file da {source} verso {dest_dir}:")
        for f in files:
            convert_one(f, dest_dir)
    elif source.is_file():
        convert_one(source, dest_dir)
    else:
        print(f"Percorso non trovato: {source}")
        sys.exit(1)


if __name__ == "__main__":
    main()
