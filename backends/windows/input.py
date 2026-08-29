"""
input.py
--------
Backend di input per Windows.

Usa l'hook globale Win32 WH_KEYBOARD_LL tramite ctypes e traduce
i Virtual-Key Code di Windows nelle categorie sonore comuni di KClick.

Questo modulo non decide se un suono debba essere riprodotto:
enabled, every_n e debounce sono responsabilità di InputController.
"""

from __future__ import annotations

import ctypes
import queue
import sys
from ctypes import wintypes


# Messaggi tastiera Win32
_WM_KEYDOWN = 0x0100
_WM_KEYUP = 0x0101
_WM_SYSKEYDOWN = 0x0104
_WM_SYSKEYUP = 0x0105
_WM_QUIT = 0x0012

# Hook / message pump
_WH_KEYBOARD_LL = 13
_PM_REMOVE = 0x0001
_QS_ALLINPUT = 0x04FF
_WAIT_FAILED = 0xFFFFFFFF

# Virtual-Key Code usati da KClick
_VK_BACK = 0x08
_VK_TAB = 0x09
_VK_RETURN = 0x0D
_VK_SHIFT = 0x10
_VK_CONTROL = 0x11
_VK_MENU = 0x12       # Alt
_VK_CAPITAL = 0x14    # Caps Lock
_VK_SPACE = 0x20
_VK_LEFT = 0x25
_VK_UP = 0x26
_VK_RIGHT = 0x27
_VK_DOWN = 0x28
_VK_SNAPSHOT = 0x2C  # Print Screen
_VK_DELETE = 0x2E
_VK_LWIN = 0x5B
_VK_RWIN = 0x5C
_VK_LSHIFT = 0xA0
_VK_RSHIFT = 0xA1
_VK_LCONTROL = 0xA2
_VK_RCONTROL = 0xA3
_VK_LMENU = 0xA4
_VK_RMENU = 0xA5

_SILENT_KEYS = {
    _VK_CONTROL,
    _VK_LCONTROL,
    _VK_RCONTROL,
    _VK_MENU,
    _VK_LMENU,
    _VK_RMENU,
    _VK_LWIN,
    _VK_RWIN,
    _VK_UP,
    _VK_DOWN,
    _VK_LEFT,
    _VK_RIGHT,
}

_SPECIAL_MAP = {
    _VK_SPACE: "space",
    _VK_RETURN: "enter",
    _VK_SHIFT: "shift",
    _VK_LSHIFT: "shift",
    _VK_RSHIFT: "shift",
    _VK_BACK: "backspace",
    _VK_DELETE: "backspace",
    _VK_TAB: "tab",
    _VK_SNAPSHOT: "printscreen",
}


class _KBDLLHOOKSTRUCT(ctypes.Structure):
    """Struttura Win32 associata agli eventi WH_KEYBOARD_LL."""

    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


def _classify_vk(vk_code: int) -> str | None:
    """
    Traduce un Virtual-Key Code Windows nella categoria sonora KClick.

    Ritorna None per i tasti volutamente silenziosi. Caps Lock usa il
    placeholder "capslock": lo stato ON/OFF viene risolto dal backend.
    """
    if vk_code == _VK_CAPITAL:
        return "capslock"
    if vk_code in _SILENT_KEYS:
        return None
    if vk_code in _SPECIAL_MAP:
        return _SPECIAL_MAP[vk_code]
    return "generic"


class WindowsInputBackend:
    """Backend Windows basato su WH_KEYBOARD_LL."""

    def run(self, stop_event, on_keypress, on_error=None) -> None:
        """
        Ascolta globalmente la tastiera finché stop_event non è impostato.

        Per ogni vera pressione (non key-up e non auto-repeat) chiama:

            on_keypress(category)

        Il callback Win32 si limita a classificare e accodare gli eventi;
        la chiamata al core avviene fuori dall'hook, per mantenerlo rapido.
        """
        if sys.platform != "win32":
            message = "WindowsInputBackend può essere eseguito solo su Windows."
            if on_error:
                on_error(message)
            return

        # WINFUNCTYPE e WinDLL esistono solo su Windows: vengono risolti qui
        # per mantenere questo modulo importabile anche durante i test Linux.
        lresult_t = ctypes.c_ssize_t
        hook_proc_t = ctypes.WINFUNCTYPE(
            lresult_t,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        )

        user32 = ctypes.WinDLL("user32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        user32.SetWindowsHookExW.argtypes = [
            ctypes.c_int,
            hook_proc_t,
            wintypes.HINSTANCE,
            wintypes.DWORD,
        ]
        user32.SetWindowsHookExW.restype = wintypes.HHOOK

        user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        user32.CallNextHookEx.restype = lresult_t

        user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
        user32.UnhookWindowsHookEx.restype = wintypes.BOOL

        user32.PeekMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
            wintypes.UINT,
        ]
        user32.PeekMessageW.restype = wintypes.BOOL

        user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
        user32.TranslateMessage.restype = wintypes.BOOL

        user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
        user32.DispatchMessageW.restype = lresult_t

        user32.MsgWaitForMultipleObjects.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(wintypes.HANDLE),
            wintypes.BOOL,
            wintypes.DWORD,
            wintypes.DWORD,
        ]
        user32.MsgWaitForMultipleObjects.restype = wintypes.DWORD

        user32.GetKeyState.argtypes = [ctypes.c_int]
        user32.GetKeyState.restype = ctypes.c_short

        kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        kernel32.GetModuleHandleW.restype = wintypes.HMODULE

        pending: queue.SimpleQueue[str] = queue.SimpleQueue()
        pressed_keys: set[int] = set()

        # GetKeyState è usato solo prima di installare l'hook. Dentro una
        # LowLevelKeyboardProc lo stato non è ancora necessariamente aggiornato.
        capslock_on = bool(user32.GetKeyState(_VK_CAPITAL) & 0x0001)

        def _hook_callback(n_code, w_param, l_param):
            nonlocal capslock_on

            if n_code >= 0:
                try:
                    event = ctypes.cast(
                        l_param,
                        ctypes.POINTER(_KBDLLHOOKSTRUCT),
                    ).contents
                    vk_code = int(event.vkCode)
                    message = int(w_param)

                    if message in (_WM_KEYUP, _WM_SYSKEYUP):
                        pressed_keys.discard(vk_code)

                    elif message in (_WM_KEYDOWN, _WM_SYSKEYDOWN):
                        # Windows genera altri KEYDOWN durante l'auto-repeat;
                        # Linux/evdev li scarta come key_hold, quindi manteniamo
                        # la stessa semantica anche qui.
                        if vk_code not in pressed_keys:
                            pressed_keys.add(vk_code)
                            category = _classify_vk(vk_code)

                            if category == "capslock":
                                capslock_on = not capslock_on
                                category = (
                                    "capslock_on"
                                    if capslock_on
                                    else "capslock_off"
                                )

                            if category is not None:
                                pending.put(category)
                except Exception:
                    # Nessuna eccezione deve attraversare un callback ctypes.
                    # Gli errori operativi vengono gestiti fuori dall'hook.
                    pass

            return user32.CallNextHookEx(
                None,
                n_code,
                w_param,
                l_param,
            )

        hook_callback = hook_proc_t(_hook_callback)
        hook = None

        try:
            module_handle = kernel32.GetModuleHandleW(None)
            hook = user32.SetWindowsHookExW(
                _WH_KEYBOARD_LL,
                hook_callback,
                module_handle,
                0,
            )

            if not hook:
                error_code = ctypes.get_last_error()
                raise OSError(
                    error_code,
                    ctypes.FormatError(error_code),
                )

            msg = wintypes.MSG()

            while not stop_event.is_set():
                wait_result = user32.MsgWaitForMultipleObjects(
                    0,
                    None,
                    False,
                    100,
                    _QS_ALLINPUT,
                )

                if wait_result == _WAIT_FAILED:
                    error_code = ctypes.get_last_error()
                    raise OSError(
                        error_code,
                        ctypes.FormatError(error_code),
                    )

                while user32.PeekMessageW(
                    ctypes.byref(msg),
                    None,
                    0,
                    0,
                    _PM_REMOVE,
                ):
                    if msg.message == _WM_QUIT:
                        return
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))

                while True:
                    try:
                        category = pending.get_nowait()
                    except queue.Empty:
                        break
                    on_keypress(category)

        except Exception as exc:
            if on_error:
                on_error(f"Errore nel backend tastiera Windows: {exc}")
        finally:
            if hook:
                user32.UnhookWindowsHookEx(hook)
