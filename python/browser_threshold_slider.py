from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtWidgets import QSizePolicy

# slider curve is y=(x/20)^3 for better resolution with lower values

# Provides: slider, threshold_label

THRESHOLD_TOOLTIP = "SD threshold"

class BrowserThresholdSlider(QObject):

    def __init__(self, change_manager):
        super(BrowserThresholdSlider, self).__init__()
        self.change_manager = change_manager
        # slider
        self.slider = QSlider()
        x=200
        self.slider.setRange(0.0, x)
        self.slider.setMinimumSize(x,4)
        self.slider.setValue(int(20*(change_manager.threshold)**(1/3)))
        self.slider.setToolTip(THRESHOLD_TOOLTIP)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setSizePolicy(QSizePolicy.Maximum,
                                         QSizePolicy.Maximum)
        self.slider.valueChanged.connect(self._handle_changed)

        # threshold_label
        self.threshold_label = QLabel("SD %.3f"%change_manager.threshold)
        self.threshold_label.setToolTip(THRESHOLD_TOOLTIP)

    @pyqtSlot(int)
    def _handle_changed(self, slider_value):
        threshold = (slider_value/20)**3
        self.threshold_label.setText("SD %.3f"%threshold)
        self.change_manager.change_threshold(threshold)

