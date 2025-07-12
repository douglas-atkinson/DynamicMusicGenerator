# DEV_NOTES.md

Dynamic Music Generator
========================

Author: Douglas Atkinson

Purpose:
--------
Track the development steps, decisions, and teaching thoughts for building the Dynamic Music Generator project for the Fall 2025 Python class.

---

## Project Timeline

### 2025-07-07

- Created `music_generator_cli.py`
    - Generates a C-major scale
    - Plays 16 random notes
    - Instrument: Piano

Teaching Notes:
- This CLI version demonstrates the pure logic behind the generator.
- Useful as a first exposure to pretty_midi.

---

### 2025-07-08

- Started planning PyQt GUI
- Discussed modularization:
    - Move music logic into `music_generator.py`
    - Keep `gui_app.py` strictly GUI

Teaching Notes:
- This is a good spot to talk about separation of concerns and code organization.
- Opportunity for an in-class lesson on modules and imports.

---

### 2025-07-11

- Coded `music_generator.py`
  - Contains functions `generate_random_melody`, `generate_scale`
  - Added dictionary for key scales
- Coded `gui_app.py`
  - Dropdown for Key
  - Button to push to generate random melody
  - Button to push to generate scale
- Snapshot
  - 02_01_music_generator.py
  - 02_02_gui_app.py

## Next Planned Steps

- Build minimal GUI with:
    - One button → generates random melody
- Gradually add:
    - Key selection dropdown
    - Tempo slider
    - Instrument dropdown
    - Note length dropdown
    - Number of notes spinner

---

## Other Thoughts

- Consider saving “snapshots” of code stages for future teaching.
- Think about whether to eventually share the repo (private vs. public).
- Magenta integration may require separate instructions due to dependencies.

