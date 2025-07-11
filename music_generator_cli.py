import pretty_midi
import random

pm = pretty_midi.PrettyMIDI()
instrument = pretty_midi.Instrument(program=0)

c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]

for i, note_number in enumerate([60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60]):
    note = pretty_midi.Note(
        velocity=100,
        pitch=note_number,
        start=i*0.5,
        end=(i+1)*0.5,
    )
    instrument.notes.append(note)

pm.instruments.append(instrument)
pm.write('scale.mid')

piano = pretty_midi.Instrument(program=0)
start_time = 0
for _ in range(16):
    note_number = random.choice(c_major_scale)
    note = pretty_midi.Note(
        velocity=100,
        pitch=note_number,
        start=start_time,
        end=start_time + 0.5
    )
    piano.notes.append(note)
    start_time += 0.5

pm.instruments.clear()
pm.instruments.append(piano)
pm.write('random_melody.mid')
