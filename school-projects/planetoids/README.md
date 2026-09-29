# Planetoids (CS 1110)

**Status:** Complete coursework game — **runnable locally** (Python 3 + Kivy).

**Course:** CS 1110 — Introduction to Computing (Cornell)

Asteroids-style arcade game built in Python with the course **game2d** library (Kivy-backed sprites and game loop). Demonstrates object-oriented design, real-time updates, vector motion, and collision handling.

---

## Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| Graphics / loop | **Kivy** via bundled `game2d/` |
| Numerics | NumPy (motion helpers in `game2d/`) |
| Assets | `Images/`, `Sounds/`, `Fonts/`, wave JSON in `Data/` |

---

## How to run

From the repository root:

```bash
cd school-projects/planetoids
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python __main__.py
```

Run commands from **`school-projects/planetoids/`** so relative paths to assets resolve correctly.

**Entry point:** `__main__.py` → `Planetoids(...).run()` in `app.py`. Keep `Images/`, `Sounds/`, `Fonts/`, and `Data/` next to the Python modules.

---

## Skills demonstrated

* Object-oriented game entities (`models.py`) and controller logic (`app.py`)
* Event-driven game loop and frame updates
* Collision detection and wave-based level data (`Data/*.json`)
* Asset management (sprites, sound effects, fonts)

---

## Project layout

```text
planetoids/
├── __main__.py      # CLI entry
├── app.py           # Main game controller
├── models.py        # Ships, asteroids, projectiles
├── consts.py        # Screen and gameplay constants
├── wave1.py         # Wave configuration helpers
├── game2d/          # Course 2D/Kivy helpers (do not relocate)
├── Data/            # Level / wave JSON
├── Images/ Sounds/ Fonts/
└── requirements.txt
```

---

## Preview (in-repo assets)

Ship sprite (representative gameplay art):

![Player ship](Images/ship.png)

For a full capture, run the game locally and add `screenshot.png` beside this README.

---

## Data note

**Academic project only.** No network services, credentials, or employer systems. All assets are local course/game files.

Parent index: [school-projects README](../README.md).
