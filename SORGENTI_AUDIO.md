# Sorgenti audio di KClick Classic

Questo file documenta la provenienza, le licenze e le principali trasformazioni
dei campioni audio distribuiti con il soundpack **KClick Classic**.

La licenza del codice sorgente di KClick è indicata separatamente nel file
`LICENSE` del repository. Le note qui sotto riguardano esclusivamente gli
asset audio inclusi in `soundpacks/KClick Classic/`.

---

## 1. kbsim

Progetto: **Mechanical Keyboard Simulator (kbsim)**  
Autore / copyright: **Thomas Lai**  
Repository: https://github.com/tplai/kbsim  
Licenza: **MIT**

Campioni utilizzati:

- `generic/alpaca_0.wav` … `alpaca_4.wav`
  - origine: `alpaca/press/GENERIC_R0.mp3` … `GENERIC_R4.mp3`
- `generic/cream_0.wav` … `cream_4.wav`
  - origine: `cream/press/GENERIC_R0.mp3` … `GENERIC_R4.mp3`
- `generic/mxbrown_0.wav` … `mxbrown_4.wav`
  - origine: `mxbrown/press/GENERIC_R0.mp3` … `GENERIC_R4.mp3`
- `generic/turquoise_0.wav` … `turquoise_4.wav`
  - origine: `turquoise/press/GENERIC_R0.mp3` … `GENERIC_R4.mp3`
- `space/space.wav`
  - origine: `alpaca/press/SPACE.mp3`
- `backspace/backspace.wav`
  - origine: `alpaca/press/BACKSPACE.mp3`

I file sono stati convertiti in WAV PCM 16-bit / 44,1 kHz e bilanciati in
livello per l'integrazione nel soundpack.

### Licenza MIT di kbsim

Copyright (c) Thomas Lai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 2. daktilo

Progetto: **daktilo**  
Autore / copyright: **Orhun Parmaksız**  
Repository: https://github.com/orhun/daktilo  
Licenza del progetto: **Apache-2.0 OR MIT, a scelta**

Per i campioni inclusi in KClick viene adottata l'opzione **MIT**.

Campioni utilizzati:

- `enter/enter.wav`
  - origine: `ding.mp3`
- `tab/tab.wav`
  - origine: `kick.mp3`

I file sono stati convertiti in WAV PCM 16-bit / 44,1 kHz e bilanciati in
livello. Il campione usato per `enter/enter.wav` è stato inoltre leggermente
smussato nelle frequenze alte per integrarsi meglio con il resto del pack.

### Licenza MIT di daktilo

Copyright © 2023-2024, Orhun Parmaksız

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 3. sound-theme-freedesktop

Progetto / pacchetto: **sound-theme-freedesktop**  
Versione di riferimento: **0.8**  
Autore / copyright dei campioni utilizzati: **Ivica Bukvic**  
Progetto upstream: https://www.freedesktop.org/wiki/Specifications/sound-theme-spec/  
Licenza dei campioni utilizzati: **Creative Commons Attribution-ShareAlike 3.0
Unported (CC BY-SA 3.0)**  
Testo della licenza: https://creativecommons.org/licenses/by-sa/3.0/

Campioni utilizzati:

- `capslock_on/capslock_on.wav`
  - origine: `stereo/device-added.oga`
- `capslock_off/capslock_off.wav`
  - origine: `stereo/device-removed.oga`
- `shift/shift.wav`
  - origine: `stereo/dialog-information.oga`

I tre campioni originali sono distribuiti in `sound-theme-freedesktop` con
copyright di Ivica Bukvic e licenza CC BY-SA 3.0.

Per KClick sono stati convertiti dal formato Ogg/Vorbis (`.oga`) a WAV PCM
16-bit / 44,1 kHz, preservando i canali stereo. Il livello è stato adattato
al resto di KClick Classic:

- `capslock_on/capslock_on.wav`: picco portato a circa **-12 dB**;
- `capslock_off/capslock_off.wav`: picco portato a circa **-12 dB**;
- `shift/shift.wav`: picco portato a circa **-17 dB**.

Non sono state applicate altre modifiche timbriche ai tre campioni.

Le versioni adattate distribuite con KClick restano soggette alla licenza
**CC BY-SA 3.0** e sono attribuite a **Ivica Bukvic**.

---

## 4. Freesound — Qat

Autore: **Qat**  
Titolo originale: **whoosh-click01.wav**  
Freesound sound ID: **108334**  
Pagina sorgente: https://freesound.org/people/Qat/sounds/108334/  
Licenza: **CC0 1.0 / Public Domain**

Campione utilizzato:

- `printscreen/printscreen.wav`

Il file è stato mantenuto nella sua interezza e convertito/bilanciato per il
soundpack.

La licenza CC0 non richiede attribuzione, ma la sorgente viene indicata qui
volontariamente per trasparenza e tracciabilità.

---

## Riepilogo

| Categoria KClick | Sorgente | Licenza |
| --- | --- | --- |
| `generic` | kbsim — Alpaca, Cream, MX Brown, Turquoise | MIT |
| `space` | kbsim — Alpaca `press/SPACE` | MIT |
| `backspace` | kbsim — Alpaca `press/BACKSPACE` | MIT |
| `shift` | sound-theme-freedesktop — `dialog-information.oga` | CC BY-SA 3.0 |
| `enter` | daktilo — `ding.mp3` | MIT |
| `tab` | daktilo — `kick.mp3` | MIT |
| `capslock_on` | sound-theme-freedesktop — `device-added.oga` | CC BY-SA 3.0 |
| `capslock_off` | sound-theme-freedesktop — `device-removed.oga` | CC BY-SA 3.0 |
| `printscreen` | Freesound — Qat, sound 108334 | CC0 1.0 |

Tutti i file distribuiti con KClick Classic provengono da sorgenti con licenze
che ne consentono la redistribuzione alle condizioni indicate sopra.
