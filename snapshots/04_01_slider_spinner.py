from PyQt5.QtWidgets import QWidget, QSlider, QSpinBox, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class SliderSpinner(QWidget):
    def __init__(self,
                 label_text="Value:",
                 min_value=0,
                 max_value=100,
                 default_value=50,
                 suffix="",
                 tick_interval=5,
                 orientation=Qt.Horizontal,
                 parent=None):
        super().__init__(parent)

        self.suffix = suffix

        # Create label text
        self.label_text = QLabel(label_text)

        # Create slider
        self.slider = QSlider(orientation)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(default_value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(tick_interval)

        # Create spinbox
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(min_value)
        self.spinbox.setMaximum(max_value)
        self.spinbox.setValue(default_value)
        self.spinbox.setSuffix(f" {suffix}".strip())

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.label_text)
        layout.addWidget(self.slider)
        layout.addWidget(self.spinbox)

        self.setLayout(layout)

        # Connect signals
        self.slider.valueChanged.connect(self._on_slider_changed)
        self.spinbox.valueChanged.connect(self._on_spinbox_changed)

    def _on_slider_changed(self, value):
        # Prevent infinite loops:
        if self.spinbox.value() != value:
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(value)
            self.spinbox.blockSignals(False)
        self.update_label(value)

    def _on_spinbox_changed(self, value):
        if self.slider.value() != value:
            self.slider.blockSignals(True)
            self.slider.setValue(value)
            self.slider.blockSignals(False)
        self.update_label(value)

    def update_label(self, value):
        # Optionally update the label text if desired
        # (Currently does nothing extra since spinbox shows value)
        pass

    def get_value(self):
        return self.spinbox.value()

    def set_value(self, value):
        """Set both slider and spinbox to a specific value."""
        self.slider.blockSignals(True)
        self.spinbox.blockSignals(True)

        self.slider.setValue(value)
        self.spinbox.setValue(value)

        self.slider.blockSignals(False)
        self.spinbox.blockSignals(False)

        self.update_label(value)

    def set_suffix(self, suffix):
        self.suffix = suffix
        self.spinbox.setSuffix(f" {suffix}".strip())

    def set_tick_interval(self, interval):
        self.slider.setTickInterval(interval)

    def set_range(self, min_value, max_value):
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.spinbox.setMinimum(min_value)
        self.spinbox.setMaximum(max_value)

    def set_orientation(self, orientation):
        self.slider.setOrientation(orientation)

    def set_tick_position(self, tick_position):
        """
        Set tick position.
        Options:
            QSlider.NoTicks
            QSlider.TicksAbove
            QSlider.TicksBelow
            QSlider.TicksBothSides
        """
        self.slider.setTickPosition(tick_position)

