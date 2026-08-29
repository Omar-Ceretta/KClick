"""
input.py
--------
Backend di input per Linux.

Legge gli eventi globali delle tastiere tramite evdev, individua
la categoria sonora KClick corrispondente e la comunica al core.

Questo modulo non decide se un suono debba essere riprodotto:
enabled, every_n e debounce sono responsabilità di InputController.
"""

from __future__ import annotations

import select

from evdev import InputDevice, categorize, ecodes, list_devices


# Tasti che KClick ignora completamente: non producono suono e non
# partecipano al conteggio every_n.
_SILENT_KEYS = {
    ecodes.KEY_LEFTCTRL,
    ecodes.KEY_RIGHTCTRL,
    ecodes.KEY_LEFTALT,
    ecodes.KEY_RIGHTALT,
    ecodes.KEY_LEFTMETA,
    ecodes.KEY_RIGHTMETA,
    ecodes.KEY_UP,
    ecodes.KEY_DOWN,
    ecodes.KEY_LEFT,
    ecodes.KEY_RIGHT,
}

# Categorie sonore speciali indipendenti dalla piattaforma.
_SPECIAL_MAP = {
    ecodes.KEY_SPACE: "space",
    ecodes.KEY_ENTER: "enter",
    ecodes.KEY_KPENTER: "enter",
    ecodes.KEY_LEFTSHIFT: "shift",
    ecodes.KEY_RIGHTSHIFT: "shift",
    ecodes.KEY_BACKSPACE: "backspace",
    ecodes.KEY_DELETE: "backspace",
    ecodes.KEY_TAB: "tab",
    ecodes.KEY_SYSRQ: "printscreen",
}


def _classify_key(keycode: int) -> str | None:
    """Traduce un keycode evdev in una categoria sonora KClick."""
    if keycode == ecodes.KEY_CAPSLOCK:
        return "capslock"
    if keycode in _SILENT_KEYS:
        return None
    return _SPECIAL_MAP.get(keycode, "generic")


def find_keyboards() -> list[InputDevice]:
    """
    Restituisce i dispositivi che sembrano tastiere.

    L'euristica considera tastiera un dispositivo capace di generare
    almeno l'evento del tasto A.
    """
    keyboards = []

    for path in list_devices():
        dev = InputDevice(path)
        caps = dev.capabilities().get(ecodes.EV_KEY, [])

        if ecodes.KEY_A in caps:
            keyboards.append(dev)
        else:
            dev.close()

    return keyboards


class LinuxInputBackend:
    """Backend Linux basato su evdev."""

    @staticmethod
    def _initial_capslock_state(keyboards: list[InputDevice]) -> bool:
        """
        Legge una sola volta lo stato iniziale di Caps Lock.

        Durante l'evento KEY_CAPSLOCK il LED del kernel può essere
        aggiornato leggermente dopo il key-down; leggerlo a ogni pressione
        renderebbe quindi possibile classificare il nuovo stato in ritardo.
        Dopo questa lettura iniziale manteniamo lo stato in memoria e lo
        invertiamo a ogni vera pressione del tasto.
        """
        for device in keyboards:
            try:
                led_caps = device.capabilities().get(ecodes.EV_LED, [])
                if ecodes.LED_CAPSL not in led_caps:
                    continue
                return ecodes.LED_CAPSL in device.leds()
            except OSError:
                continue
        return False

    def run(self, stop_event, on_keypress, on_error=None) -> None:
        """
        Ascolta le tastiere finché stop_event non viene impostato.

        Per ogni pressione valida chiama:

            on_keypress(category)

        dove category è una categoria sonora indipendente dalla
        piattaforma.
        """
        try:
            keyboards = find_keyboards()
        except Exception as exc:
            if on_error:
                on_error(
                    f"Impossibile aprire i dispositivi tastiera: {exc}"
                )
            return

        if not keyboards:
            if on_error:
                on_error("Nessuna tastiera trovata su /dev/input.")
            return

        devices_by_fd = {dev.fd: dev for dev in keyboards}
        capslock_on = self._initial_capslock_state(keyboards)

        try:
            while not stop_event.is_set():
                ready, _, _ = select.select(
                    devices_by_fd,
                    [],
                    [],
                    0.5,
                )

                for fd in ready:
                    device = devices_by_fd[fd]

                    for event in device.read():
                        if event.type != ecodes.EV_KEY:
                            continue

                        key_event = categorize(event)

                        if key_event.keystate != key_event.key_down:
                            continue

                        category = _classify_key(event.code)

                        if category is None:
                            continue

                        if category == "capslock":
                            capslock_on = not capslock_on
                            category = (
                                "capslock_on"
                                if capslock_on
                                else "capslock_off"
                            )

                        on_keypress(category)

        finally:
            for device in keyboards:
                device.close()
