import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QMessageBox, QComboBox
)
import music_generator

class MelodyGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dynamic Music Generator")

        layout = QVBoxLayout()

        #Dropdown for key selection
        self.key_combo = QComboBox()
        self.key_combo.addItems(music_generator.KEY_SCALES_MAJOR.keys())

        # Button for random melody
        self.melody_button = QPushButton("Generate Random Melody")
        self.melody_button.clicked.connect(self.generate_melody)

        # Button for scale
        self.scale_button = QPushButton("Generate Scale")
        self.scale_button.clicked.connect(self.generate_scale)

        layout.addWidget(self.key_combo)
        layout.addWidget(self.melody_button)
        layout.addWidget(self.scale_button)

        self.setLayout(layout)
        self.resize(300, 200)

    def generate_melody(self):
        try:
            print("Generating Melody")
            selected_key = self.key_combo.currentText()

            #key_scale = music_generator.KEY_SCALES_MAJOR[selected_key].get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])
            key_scale = music_generator.KEY_SCALES_MAJOR.get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])

            filename = music_generator.generate_random_melody(key_scale=key_scale)

            QMessageBox.information(self, "Done", f"Melody saved as {filename}")
        except Exception as e:
            print("Error: ", e)
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def generate_scale(self):
        try:
            selected_key = self.key_combo.currentText()

            #key_scale = music_generator.KEY_SCALES_MAJOR[selected_key].get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])
            key_scale = music_generator.KEY_SCALES_MAJOR.get(selected_key, music_generator.KEY_SCALES_MAJOR['C Major'])

            filename = music_generator.generate_scale(key_scale=key_scale)

            QMessageBox.information(self, "Done", f"Scale saved as {filename}")
        except Exception as e:
            print("Error: ", e)
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MelodyGenerator()
    window.show()
    sys.exit(app.exec_())

