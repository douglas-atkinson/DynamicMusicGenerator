import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox, QMenuBar, QFileDialog
)
import music_generator

class MelodyGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.loaded_midi_path = None   # Store loaded MIDI file
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dynamic Music Generator")

        layout = QVBoxLayout()

        # Menu Bar
        menu_bar = QMenuBar()

        file_menu = menu_bar.addMenu("File")
        load_action = file_menu.addAction("Load MIDI File...")
        load_action.triggered.connect(self.load_midi_file)

        layout.setMenuBar(menu_bar)

        #Dropdown for key selection
        self.key_combo = QComboBox()
        self.key_combo.addItems(music_generator.KEY_SCALES_MAJOR.keys())

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

        layout.addWidget(self.key_combo)
        layout.addWidget(self.melody_button)
        layout.addWidget(self.scale_button)
        layout.addWidget(self.play_button)

        self.setLayout(layout)
        self.resize(400, 250)

    def generate_melody(self):
        try:
            print("Generating Melody")
            selected_key = self.key_combo.currentText()

            key_scale = music_generator.KEY_SCALES_MAJOR.get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])

            filename = music_generator.generate_random_melody(key_scale=key_scale)

            QMessageBox.information(self, "Done", f"Melody saved as {filename}")
        except Exception as e:
            print("Error: ", e)
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def generate_scale(self):
        try:
            selected_key = self.key_combo.currentText()

            key_scale = music_generator.KEY_SCALES_MAJOR.get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])

            filename = music_generator.generate_scale(key_scale=key_scale)

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

