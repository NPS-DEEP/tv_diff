
"""Manages graph scale.

Provides the following services:

  global const original_scale provides startng value, unity 1.0.
  signal_tv_scale_changed provides changed tv scale.

  Use interfaces:
     scale_in, scale_out, scale_original
"""
from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSignal, pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt

# default
original_scale = 1.0 # const

class TVScaleManager(QObject):

    # signal
    signal_tv_scale_changed = pyqtSignal(float, name='TVScaleChanged')

    def __init__(self):
        super(TVScaleManager, self).__init__()
        self._scale = original_scale

    def scale_in(self):
        self._scale *=2.0
        # signal change
        self.signal_tv_scale_changed.emit(self._scale)

    def scale_out(self):
        self._scale /=2.0
        # signal change
        self.signal_tv_scale_changed.emit(self._scale)

    def scale_original(self):
        self._scale = original_scale
        # signal change
        self.signal_tv_scale_changed.emit(self._scale)

