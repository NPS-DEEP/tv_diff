from show_popup import show_popup
import json
from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSignal # for signal/slot support
from PyQt5.QtCore import pyqtSlot # for signal/slot support

from read_tv_file import read_tv_file
from settings_store import texture_compatible
from similarity_math import generate_similarity_data, empty_similarity_data

"""Provides data and signals.

Data structures:
tv_data1
tv_data2

step = int

similarity_lines = dict<index, list<index>>
similarity_histogram = dict<bucket, count>
similarity_sd = float f(similarity_histogram)
similarity_mean = float f(similarity_histogram)

Signals:
  * signal_data_loaded(data structures)
    - data1
    - data2
    - step
    - similarity_data<dict>
"""

class TVDataManager(QObject):

    # signals
    signal_data_loaded = pyqtSignal(dict, dict, int, dict,
                                    name='dataLoaded')

    def __init__(self, settings, signal_settings_changed):
        super(TVDataManager, self).__init__()

        self.settings = settings

        # connect to reset data on settings change
        signal_settings_changed.connect(self.change_settings)

        # set initial state
        self.tv_data1 = dict()
        self.tv_data2 = dict()
        self.step = 1

    def _read_tv_file(self, filename):
        try:
            return read_tv_file(filename)

        except Exception as e:
            show_popup(None, "Error reading .tv file '%s': %s"%(filename, e))
            return dict()

    # recalculate and signal
    def _reset_data(self):
        try:
            similarity_data = generate_similarity_data(
                                         self.tv_data1, self.tv_data2,
                                         self.step, self.settings, True)
            self.signal_data_loaded.emit(self.tv_data1, self.tv_data2,
                                         self.step, similarity_data)
        except Exception as e:
            self.signal_data_loaded.emit(self.tv_data1, self.tv_data2,
                                         self.step, empty_similarity_data())
            show_popup(None, "Error processing .tv data: %s"%str(e))

    def set_tv_data1(self, tv_filename):
        self.tv_data1 = self._read_tv_file(tv_filename)
        self._reset_data()

    def set_tv_data2(self, tv_filename):
        self.tv_data2 = self._read_tv_file(tv_filename)
        self._reset_data()

    def set_tv_data_pair(self, tv_filename1, tv_filename2):
        if tv_filename1:
            self.tv_data1 = self._read_tv_file(tv_filename1)
        else:
            self.tv_data1 = dict()
        if tv_filename2:
            self.tv_data2 = self._read_tv_file(tv_filename2)
        else:
            self.tv_data2 = dict()
        self._reset_data()

    # hardcoded interpretation of sketch quantity
    @pyqtSlot(dict)
    def change_settings(self, settings):
        self.settings = settings
        self._reset_data()

    # hardcoded interpretation of sketch quantity
    @pyqtSlot(bool)
    def toggle_draw_sketch(self, draw_sketch):
        if draw_sketch:
            self.step = 50
        else:
            self.step = 1
        self._reset_data()

