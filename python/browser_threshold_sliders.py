from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QWidget, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QSizePolicy

# SD slider curve is y=(x/20)^3 for better resolution with lower values

# Provides: sd_slider, sd_threshold_label

class BrowserThresholdSliders(QWidget):

    def __init__(self, change_manager):
        super(BrowserThresholdSliders, self).__init__()
        self.change_manager = change_manager

        # slider width
        x=200

        # SD slider
        self.sd_slider = QSlider()
        self.sd_slider.setRange(0.0, x)
        self.sd_slider.setMinimumSize(x,4)
        self.sd_slider.setValue(int(20*(change_manager.sd_threshold)**(1/3)))
        self.sd_slider.setToolTip("Standard Deviation threshold")
        self.sd_slider.setOrientation(Qt.Horizontal)
        self.sd_slider.setSizePolicy(QSizePolicy.Maximum,
                                         QSizePolicy.Maximum)
        self.sd_slider.valueChanged.connect(self._handle_sd_changed)

        # SD threshold_label
        self.sd_threshold_label = QLabel("Std. Dev. %.3f"%change_manager.sd_threshold)
        self.sd_threshold_label.setToolTip("Standard Deviation threshold")

        # layout management
        layout = QGridLayout()
        layout.addWidget(self.sd_slider,0,0)
        layout.addWidget(self.sd_threshold_label,0,1)
        self.setLayout(layout)

    @pyqtSlot(int)
    def _handle_sd_changed(self, slider_value):
        sd_threshold = (slider_value/20)**3
        self.sd_threshold_label.setText("SD %.3f"%sd_threshold)
        self.change_manager.change_sd_threshold(sd_threshold)

