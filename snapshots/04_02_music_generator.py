# music_generator.py
# version 0.1

import pretty_midi
import random

KEY_SCALES_MAJOR = {
    'C Major': [60, 62, 64, 65, 67, 69, 71, 72],
    'G Major': [67, 69, 71, 72, 74, 76, 78, 79],
    'D Major': [62, 64, 66, 67, 69, 71, 73, 74],
    'A Major': [69, 71, 73, 74, 76, 78, 80, 81],
    'F Major': [65, 67, 69, 70, 72, 74, 76, 77],
    'Bb Major': [70, 72, 74, 75, 77, 79, 81, 82],
    'Eb Major': [63, 65, 67, 68, 70, 72, 74, 75],
}

INSTRUMENTS = {
    "Acoustic Grand Piano": 0,
    "Violin": 40,
    "Trumpet": 56,
    "Flute": 73,
    "Electric Guitar (clean)": 27
}

NOTE_LENGTHS = {
    "Whole": 4.0,
    "Half": 2.0,
    "Quarter": 1.0,
    "Eight": 0.5,
    "Sixteenth": 0.25
}

def generate_scale(
        filename="scale.mid",
        key_scale=None,
        tempo=120,
        note_length_fraction=1.0,
        instrument_program=0
):
    """
    Generate an ascending and descending scale and save it to a MIDI file.

    :param filename: (str) Output MIDI filename
    :param key_scale: (list[int]) list of MIDI note numbers for the scale
    :param tempo: (int) Tempo in BPM
    :param note_length_fraction: (float) Multiplier for note duration (1.0 = quarter note)
    :param instrument_program: (int) MIDI program number (instrument)
    :return:
    """

    # Default to C major if not provided
    if key_scale is None:
        key_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C Major

    quarter_duration = 60 / tempo * note_length_fraction

    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    instrument = pretty_midi.Instrument(program=instrument_program)

    # Go up the scale
    start_time = 0
    for note_number in key_scale[:-1]:
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=start_time,
            end=start_time + quarter_duration
        )
        instrument.notes.append(note)
        start_time = start_time + quarter_duration

    # Tonic note (top)
    note = pretty_midi.Note(
        velocity=100,
        pitch=key_scale[-1],
        start=start_time,
        end=start_time + quarter_duration * 2
    )
    instrument.notes.append(note)
    start_time = start_time + quarter_duration * 2

    # Descending (omit duplicate tonic at start)
    descending_scale = list(reversed(key_scale))
    descending_scale.pop(0)


    for note_number in descending_scale[:-1]:
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=start_time,
            end=start_time + quarter_duration
        )
        instrument.notes.append(note)
        start_time = start_time + quarter_duration

    # Tonic note (end)
    note = pretty_midi.Note(
        velocity=100,
        pitch=descending_scale[-1],
        start=start_time,
        end=start_time + quarter_duration * 2
    )
    instrument.notes.append(note)

    pm.instruments.append(instrument)
    pm.write(filename)

    return filename


def generate_random_melody(
        filename="random_melody.mid",
        key_scale=None,
        tempo=120,
        note_count=16,
        note_length_fraction=1.0,
        instrument_program=0
):
    """
    Generate a random melody with specified key scale and tempo and save it to a MIDI file.

    :param filename: (str) Output MIDI filename
    :param key_scale: (list[int]) list of MIDI note numbers for the scale
    :param tempo:  (int) Tempo in BPM
    :param note_count: (int) Number of notes to generate
    :param note_length_fraction: (float) Multiplier for note duration (1.0 = quarter note)
    :param instrument_program: (int) MIDI program number (instrument)
    :return: filename: (str) MIDI filename
    """

    # Default to C major if not provided
    if key_scale is None:
        key_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C Major

    quarter_duration = 60 / tempo * note_length_fraction

    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    instrument = pretty_midi.Instrument(program=instrument_program)

    start_time = 0
    for _ in range(note_count):
        note_number = random.choice(key_scale)
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=start_time,
            end=start_time + quarter_duration,
        )
        instrument.notes.append(note)
        start_time = start_time + quarter_duration

    pm.instruments.append(instrument)
    pm.write(filename)

    return filename