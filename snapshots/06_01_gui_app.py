# gui_app.py

import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox, QMenuBar, QFileDialog,
    QFormLayout, QSpinBox
)
from PyQt5.QtCore import Qt

import music_generator
from music_generator import INSTRUMENTS, NOTE_LENGTHS, generate_scale, generate_random_melody, generate_melody_rule_based
from slider_spinner import SliderSpinner

class MelodyGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.loaded_midi_path = None   # Store loaded MIDI file
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dynamic Music Generator")

        # Layouts
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Controls
        self.key_dropdown = QComboBox()
        self.key_dropdown.addItems([
            'C Major', 'D Major', 'E Major', 'F Major',
            'G Major', 'A Major', 'B Major', 'Bb Major', 'Eb Major'
        ])

        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems([
            'Scale', 'Random Melody', 'Rule-Based Melody'
        ])

        self.instrument_dropdown = QComboBox()
        self.instrument_dropdown.addItems(INSTRUMENTS.keys())

        self.note_length_dropdown = QComboBox()
        self.note_length_dropdown.addItems(NOTE_LENGTHS.keys())

        self.tempo_control = SliderSpinner(label_text="Tempo", min_value=60, max_value=240, default_value=120,
                                           tick_interval=20)
        self.num_notes_spinner = QSpinBox()
        self.num_notes_spinner.setRange(4, 64)
        self.num_notes_spinner.setValue(16)

        # Buttons
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_music)

        self.load_button = QPushButton("Load MIDI")
        self.load_button.clicked.connect(self.load_midi_file)

        self.play_button = QPushButton("Play MIDI")
        self.play_button.clicked.connect(self.play_loaded_midi)
        self.play_button.setEnabled(False)

        # Add widgets to layout
        self.form_layout.addRow("Key:", self.key_dropdown)
        self.form_layout.addRow("Mode:", self.mode_dropdown)
        self.form_layout.addRow("Instrument:", self.instrument_dropdown)
        self.form_layout.addRow("Note Length:", self.note_length_dropdown)
        self.form_layout.addRow("Tempo:", self.tempo_control)
        self.form_layout.addRow("Number of Notes:", self.num_notes_spinner)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.play_button)

        self.setLayout(self.layout)

    def generate_music(self):
        key = self.key_dropdown.currentText()
        instrument_name = self.instrument_dropdown.currentText()
        instrument = INSTRUMENTS[instrument_name]
        note_length_name = self.note_length_dropdown.currentText()
        note_length = NOTE_LENGTHS[note_length_name]
        tempo = self.tempo_control.get_value()
        num_notes = self.num_notes_spinner.value()
        mode = self.mode_dropdown.currentText()

        self.filename = f"output_{key.replace(' ', '_')}_{mode.lower().replace(' ', '_')}.mid"

        print("In generate_music")

        print(f"[DEBUG] Mode: {mode}, Key: {key}, Tempo: {tempo}, Note Length: {note_length}, Instrument: {instrument}, Notes: {num_notes}")

        try:

            if mode == 'Scale':
                generate_scale(
                    filename=self.filename,
                    key_name=key,
                    tempo=tempo,
                    note_length_fraction=note_length,
                    instrument_program=instrument
                )

            elif mode == 'Random Melody':
                generate_random_melody(
                    filename=self.filename,
                    key_name=key,
                    tempo=tempo,
                    note_length_fraction=note_length,
                    instrument_program=instrument,
                    note_count=num_notes
                )

            elif mode == 'Rule-Based Melody':
                generate_melody_rule_based(
                    filename=self.filename,
                    key_name=key,
                    tempo=tempo,
                    note_length_fraction=note_length,
                    instrument_program=instrument,
                    note_count=num_notes
                )

        except Exception as e:
            print("Error: ", e)

        QMessageBox.information(self, "MIDI Generated", f"MIDI file saved as {self.filename}")
        # self.play_button.setEnabled(True)

    def load_midi_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select a MIDI File",
            "",
            "MIDI Files (*.mid *.midi)",
            options=options,
        )
        if file_name:
            self.loaded_midi_path = file_name
            self.play_button.setEnabled(True)
            QMessageBox.information(
                self,
                "File Loaded",
                f"Loaded MIDI file: {self.loaded_midi_path}",
            )

    def play_loaded_midi(self):
        if self.loaded_midi_path:
            try:
                subprocess.run(["start", "", self.loaded_midi_path], shell=True, check=True)

            except Exception as e:
                print("Error: ", e)
                QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
        else:
            QMessageBox.critical(self, "No File", "Please load a MIDI file first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MelodyGenerator()
    window.show()
    sys.exit(app.exec_())

