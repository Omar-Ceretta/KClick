"""
sound_categories.py
-------------------
Definisce le categorie sonore conosciute da KClick.

Queste categorie sono indipendenti dal sistema operativo:
i backend Linux e Windows traducono i rispettivi eventi di tastiera
in uno di questi nomi, che l'AudioEngine usa per scegliere il suono.
"""

ALL_CATEGORIES = [
    "generic",
    "space",
    "enter",
    "shift",
    "backspace",
    "tab",
    "capslock_on",
    "capslock_off",
    "printscreen",
]
