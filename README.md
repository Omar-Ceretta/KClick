# KClick

**KClick** aggiunge un feedback sonoro alla digitazione, trasformando i tasti in una piccola tastiera meccanica virtuale.

È un'applicazione leggera in Python con interfaccia **PySide6**, pensata per funzionare in background dalla system tray su **Linux** e **Windows**.

## Caratteristiche

- riproduzione globale dei suoni durante la digitazione;
- soundpack predefinito **KClick Classic**;
- 20 varianti per i tasti generici, scelte casualmente senza ripetere due volte di seguito lo stesso campione;
- suoni dedicati per:
  - Spazio;
  - Invio;
  - Shift;
  - Backspace / Canc;
  - Tab;
  - Caps Lock ON / OFF;
  - Print Screen;
- Ctrl, Alt, Meta e frecce direzionali volutamente silenziosi;
- regolazione del volume;
- possibilità di far suonare una battuta ogni *N* pressioni;
- intervallo minimo configurabile tra due suoni;
- attivazione/disattivazione immediata dalla tray;
- autostart opzionale al login;
- icone tray adattate a tema chiaro e scuro;
- configurazione salvata localmente nella cartella di KClick.

## KClick Classic

Il soundpack incluso nasce da una selezione e da un bilanciamento di campioni provenienti da progetti e archivi con licenze compatibili con la redistribuzione.

Le sorgenti, le attribuzioni, le licenze e le trasformazioni applicate ai file audio sono documentate in [`SORGENTI_AUDIO.md`](SORGENTI_AUDIO.md).

## Requisiti

- Python **3.10 o successivo**
- PySide6
- pygame
- evdev su Linux

Le dipendenze Python sono elencate in `requirements.txt`.

Su Linux KClick legge gli eventi globali della tastiera tramite `evdev`: l'utente deve quindi avere i permessi necessari per leggere i dispositivi di input del sistema.

## Avvio da sorgente

### Linux

```bash
git clone https://github.com/Omar-Ceretta/KClick.git
cd KClick

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python kclick.py
```

### Windows

Da PowerShell:

```powershell
git clone https://github.com/Omar-Ceretta/KClick.git
cd KClick

py -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python kclick.py
```

Una volta avviato, KClick resta nella **system tray**.

- **click sinistro** sull'icona: attiva/disattiva i suoni;
- **click destro**: apre il menu con Impostazioni ed Esci.

## Impostazioni

La finestra delle impostazioni permette di modificare in tempo reale:

- soundpack;
- volume;
- frequenza dei suoni (`1` battuta ogni `N`);
- intervallo minimo tra due suoni;
- avvio automatico al login.

Le preferenze vengono salvate in `config.json`, creato automaticamente nella radice dell'applicazione. Il file è locale e non viene versionato nel repository.

L'autostart usa:

- **systemd --user** su Linux;
- la chiave **Run** dell'utente su Windows.

## Struttura essenziale

```text
KClick/
├── backends/          # input e autostart specifici per Linux/Windows
├── core/              # configurazione, audio e controllo degli eventi
├── gui/               # finestra impostazioni, tray e icone
├── soundpacks/
│   └── KClick Classic/
├── kclick.py
├── requirements.txt
├── SORGENTI_AUDIO.md
└── LICENSE
```

## Licenza

Il codice di KClick è distribuito sotto licenza **GNU General Public License v3.0**. Vedi [`LICENSE`](LICENSE).

Gli asset audio inclusi in **KClick Classic** provengono da fonti con licenze proprie; i dettagli sono raccolti in [`SORGENTI_AUDIO.md`](SORGENTI_AUDIO.md).

---

KClick è un progetto indipendente e open source.
