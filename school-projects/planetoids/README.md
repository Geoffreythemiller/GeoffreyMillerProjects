# Planetoids (CS 1110)

**Course:** CS 1110 — Introduction to Computing (Cornell)

Asteroids-style arcade game built in Python with a custom 2D game library (`game2d/`). Demonstrates object-oriented design, real-time game loops, vector motion, and collision handling.

## Stack

* **Python 3**
* **game2d** — course graphics/sprite layer (included in this folder)
* Asset folders: `Images/`, `Sounds/`, `Fonts/`, level data in `Data/`

## How to run

From the repository root:

```bash
cd school-projects/planetoids
python __main__.py
```

Run from **`school-projects/planetoids/`** so relative paths to `Images/`, `Sounds/`, and `Data/` resolve correctly.

**Entry point:** `__main__.py` launches `Planetoids(...).run()` from `app.py`. Keep `Images/`, `Sounds/`, `Fonts/`, and `Data/` alongside the Python modules — moving them breaks asset loading.

## Project layout (high level)

```text
planetoids/
├── __main__.py      # CLI entry
├── app.py           # Main game controller
├── models.py        # Game entities
├── consts.py        # Screen and gameplay constants
├── game2d/          # 2D rendering helpers
├── Data/            # Wave/level JSON
├── Images/ Sounds/ Fonts/
```

## Screenshot

*(Optional: add `screenshot.png` here when capturing gameplay locally.)*

Parent index: [school-projects README](../README.md).
