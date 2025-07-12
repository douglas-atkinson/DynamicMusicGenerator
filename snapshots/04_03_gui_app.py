# gui_app.py

import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox, QMenuBar, QFileDialog,
    QFormLayout, QSpinBox
)
from PyQt5.QtCore import Qt
import music_generator
from slider_spinner import SliderSpinner

class MelodyGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.loaded_midi_path = None   # Store loaded MIDI file
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dynamic Music Generator")

        main_layout = QVBoxLayout()

        # Menu Bar
        menu_bar = QMenuBar()

        file_menu = menu_bar.addMenu("File")
        load_action = file_menu.addAction("Load MIDI File...")
        load_action.triggered.connect(self.load_midi_file)

        main_layout.setMenuBar(menu_bar)

        # Form layout
        form_layout = QFormLayout()

        #Dropdown for key selection
        self.key_combo = QComboBox()
        self.key_combo.addItems(music_generator.KEY_SCALES_MAJOR.keys())
        form_layout.addRow("key:", self.key_combo)

        # Tempo slider+spinner
        self.temp_control = SliderSpinner(
            label_text="Tempo:",
            min_value=60,
            max_value=240,
            default_value=120,
            suffix=" BMP",
            tick_interval=10,
            orientation=Qt.Horizontal
        )
        form_layout.addRow("Tempo:", self.temp_control)

        #instrument dropdown
        self.instrument_combo = QComboBox()
        self.instrument_combo.addItems(music_generator.INSTRUMENTS.keys())
        form_layout.addRow("Instrument:", self.instrument_combo)

        # Note length dropdown
        self.note_length_combo = QComboBox()
        self.note_length_combo.addItems(music_generator.NOTE_LENGTHS.keys())
        form_layout.addRow("Note Length:", self.note_length_combo)

        # Number of notes spinner
        self.num_notes_spinner = QSpinBox()
        self.num_notes_spinner.setMinimum(4)
        self.num_notes_spinner.setMaximum(64)
        self.num_notes_spinner.setValue(16)
        form_layout.addRow("Number of Notes:", self.num_notes_spinner)

        main_layout.addLayout(form_layout)

        # Buttons
        # Button for random melody
        self.melody_button = QPushButton("Generate Random Melody")
        self.melody_button.clicked.connect(self.generate_melody)

        # Button for scale
        self.scale_button = QPushButton("Generate Scale")
        self.scale_button.clicked.connect(self.generate_scale)

        # Button to play loaded MIDI file
        self.play_button = QPushButton("Play Loaded MIDI")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play_loaded_midi)

        # Add buttons to layout
        main_layout.addWidget(self.melody_button)
        main_layout.addWidget(self.scale_button)
        main_layout.addWidget(self.play_button)

        self.setLayout(main_layout)
        self.resize(500, 300)

    def generate_melody(self):
        try:
            selected_key = self.key_combo.currentText()
            tempo = self.temp_control.get_value()
            instrument_name = self.instrument_combo.currentText()
            instrument_program = music_generator.INSTRUMENTS[instrument_name]
            note_length_name = self.note_length_combo.currentText()
            note_length_fraction = music_generator.NOTE_LENGTHS[note_length_name]
            num_notes = self.num_notes_spinner.value()
            key_scale = music_generator.KEY_SCALES_MAJOR.get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])

            filename = music_generator.generate_random_melody(
                key_scale=key_scale,
                tempo=tempo,
                instrument_program=instrument_program,
                note_length_fraction=note_length_fraction,
                note_count=num_notes
            )

            QMessageBox.information(self, "Done", f"Melody saved as {filename}")
        except Exception as e:
            print("Error: ", e)
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def generate_scale(self):
        try:
            selected_key = self.key_combo.currentText()
            key_scale = music_generator.KEY_SCALES_MAJOR.get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])
            tempo = self.temp_control.get_value()
            instrument_name = self.instrument_combo.currentText()
            instrument_program = music_generator.INSTRUMENTS[instrument_name]
            note_length_name = self.note_length_combo.currentText()
            note_length_fraction = music_generator.NOTE_LENGTHS[note_length_name]

            filename = music_generator.generate_scale(
                key_scale=key_scale,
                tempo=tempo,
                instrument_program=instrument_program,
                note_length_fraction=note_length_fraction,
            )

            QMessageBox.information(self, "Done", f"Scale saved as {filename}")
        except Exception as e:
            print("Error: ", e)
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

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

