"""
Backend specifici del sistema operativo.

Il resto di KClick importa da qui le funzionalità dipendenti
dalla piattaforma senza conoscere la loro implementazione.
"""

import sys


if sys.platform.startswith("linux"):
    from .linux.input import LinuxInputBackend as InputBackend
    from .linux.autostart import set_autostart
elif sys.platform == "win32":
    from .windows.input import WindowsInputBackend as InputBackend
    from .windows.autostart import set_autostart
else:
    raise NotImplementedError(
        f"Sistema operativo non supportato: {sys.platform}"
    )
