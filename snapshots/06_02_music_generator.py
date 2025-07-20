# music_generator.py
# version 0.1

import pretty_midi
import random

import scale_library
from scale_library import ScaleLibrary

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

KEY_SCALES_MAJOR = ScaleLibrary.major_scales()

def generate_scale(
        filename="scale.mid",
        key_name="C Major",
        tempo=120,
        note_length_fraction=1.0,
        instrument_program=0
):
    """
    Generate an ascending and descending scale and save it to a MIDI file.

    :param filename: (str) Output MIDI filename
    :param key_name: (str) name of the key to generate scale with
    :param tempo: (int) Tempo in BPM
    :param note_length_fraction: (float) Multiplier for note duration (1.0 = quarter note)
    :param instrument_program: (int) MIDI program number (instrument)
    :return:
    """

    key_scale = ScaleLibrary.major_scales()[key_name]

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
        key_name="C Major",
        tempo=120,
        note_count=16,
        note_length_fraction=1.0,
        instrument_program=0
):
    """
    Generate a random melody with the specified key scale and tempo and save it to a MIDI file.

    :param filename: (str) Output MIDI filename
    :param key_name: (str) Name of the key to generate melody with
    :param tempo:  (int) Tempo in BPM
    :param note_count: (int) Number of notes to generate
    :param note_length_fraction: (float) Multiplier for note duration (1.0 = quarter note)
    :param instrument_program: (int) MIDI program number (instrument)
    :return: filename: (str) MIDI filename
    """

    key_scale = ScaleLibrary.major_scales()[key_name]

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

def generate_melody_rule_based(
        filename=None,
        key_name="C Major",
        tempo=120,
        instrument_program=0,
        note_length_fraction=1.0,
        note_count=16,
        leap_probability=0.1,
        max_leap_size=4,
        contour="arch"
):
    """
    Generate a melody in the chosen key using stepwise motion and occasional leaps

    :param filename: (str) MIDI filename
    :param key_name: (str) Name of the key to generate melody with
    :param tempo: (int) Tempo in BPM
    :param instrument_program: (int) MIDI program number (instrument)
    :param note_length_fraction: (float) Multiplier for note duration (1.0 = quarter note)
    :param note_count: (int) Number of notes to generate
    :param leap_probability: (float) Probability of occasional leaps instead of steps
    :param max_leap_size: (int) Maximum leap size in scale degrees
    :param contour: (str) 'arch', 'ascending', 'descending', or 'random'
    :return: (str) Filename generated MIDI file
    """

    key_scale = ScaleLibrary.major_scales()[key_name]
    scale_length = len(key_scale)

    # start on tonic
    current_index = scale_length // 2
    melody_indices = [current_index]

    for i in range(1, note_count):
        # Decide contour direction
        if contour == "arch":
            if i < note_count / 2:
                step_options = [1, 2]
            else:
                step_options = [-2, -1]
        elif contour == "ascending":
            step_options = [1, 2]
        elif contour == "descending":
            step_options = [-2, -1]
        else:
            step_options = [-2, -1, 0, 1, 2]

        if random.random() < leap_probability:
            step = random.choice(
                [s for s in range(-max_leap_size, max_leap_size + 1) if s != 0]
            )
        else:
            step = random.choice(step_options)

        new_index = current_index + step

        # Clamp to scale boundaries
        next_index = max(0, min(scale_length - 1, new_index))

        melody_indices.append(next_index)
        current_index = next_index

    # generate MIDI
    quarter_duration = 60 / tempo * note_length_fraction

    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    instrument = pretty_midi.Instrument(program=instrument_program)

    start_time = 0
    for idx in melody_indices:
        note_number = key_scale[idx]
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=start_time,
            end=start_time + quarter_duration
        )
        instrument.notes.append(note)
        start_time = start_time + quarter_duration

    pm.instruments.append(instrument)

    if filename is None:
        filename = f"rule_based_melody_{key_name.replace(' ', '_')}.mid"

    pm.write(filename)
    return filename

