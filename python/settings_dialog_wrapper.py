# wrapper from https://stackoverflow.com/questions/2398800/linking-a-qtdesigner-ui-file-to-python-pyqt
import os
from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSlot # for signal/slot support
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialogButtonBox
from settings_dialog import Ui_SettingsDialog
from settings_manager import default_settings
from show_popup import show_popup

# user's preferred Settings path
preferred_settings_dir = os.path.expanduser("~")

# a suggested settings filename
def _suggested_settings_filename():
    return os.path.join(preferred_settings_dir, "tv_threshold_settings.stg")

class SettingsDialogWrapper(QDialog):
    def _set_starting_settings(self):

        # old setings
        self.old_settings = self.settings_manager.copy()

        try:
            s=self.old_settings
            self.ui.rejection_slider.setValue(s["rejection_threshold"]*10)
            self.ui.slider0.setValue(int(s["sd_weight"]*1000))
            self.ui.slider1.setValue(int(s["mean_weight"]*1000))
            self.ui.slider2.setValue(int(s["mode_weight"]*1000))
            self.ui.slider3.setValue(int(s["mode_count_weight"]*1000))
            self.ui.slider4.setValue(int(s["entropy_weight"]*1000))
        except KeyError as e:
            show_popup(None, "Error restoring settings: %s" % str(e))

    def __init__(self, parent, settings_manager):
        super(SettingsDialogWrapper, self).__init__(parent)
        self.parent = parent
        self.settings_manager = settings_manager
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self._set_starting_settings()

        # load/save
        self.ui.load_pb.clicked.connect(self.load_pb_clicked)
        self.ui.save_pb.clicked.connect(self.save_pb_clicked)

        # connect
        self.ui.rejection_slider.sliderMoved.connect(
                                            self.rejection_slider_moved)
        self.ui.slider0.sliderMoved.connect(self.slider0_moved)
        self.ui.slider1.sliderMoved.connect(self.slider1_moved)
        self.ui.slider2.sliderMoved.connect(self.slider2_moved)
        self.ui.slider3.sliderMoved.connect(self.slider3_moved)
        self.ui.slider4.sliderMoved.connect(self.slider4_moved)

        # cancel
        self.ui.button_box.rejected.connect(self.cancel)

        # restore defaults
        self.ui.button_box.button(
                         QDialogButtonBox.RestoreDefaults).clicked.connect(
                                                     self.restore_defaults)

    def closeEvent(self, e):
        # abort by restoring settings when user deliberately closes the window
        self.settings_manager.change_all(self.old_settings)

    @pyqtSlot()
    def restore_defaults(self):
        # restore to default
        self.settings_manager.change_all(default_settings)
        self._set_starting_settings()

    @pyqtSlot()
    def cancel(self):
        # restore to before
        self.settings_manager.change_all(self.old_settings)

    # load settings
    @pyqtSlot()
    def load_pb_clicked(self):
        global preferred_settings_dir
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        settings_filename, _ = QFileDialog.getOpenFileName(self.parent,
                        "Load TV GUI settings file",
                        _suggested_settings_filename(),
                        "TV GUI Settings files (*.stg);;All Files (*)",
                        options=options)

        if settings_filename:

            # remember the preferred path
            head, _tail = os.path.split(settings_filename)
            preferred_settings_dir = head

            # load settings from file
            self.settings_manager.load_from(settings_filename)

    # save settings
    @pyqtSlot()
    def save_pb_clicked(self):
        global preferred_settings_dir
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        settings_filename, _ = QFileDialog.getSaveFileName(self.parent,
                        "Save TV GUI settings file",
                        _suggested_settings_filename(),
                        "TV GUI Settings files (*.stg);;All Files (*)",
                        options=options)

        if settings_filename:

            # remember the preferred path
            head, _tail = os.path.split(settings_filename)
            preferred_settings_dir = head

            # save settings to file
            self.settings_manager.save_to(settings_filename)

    # slider
    @pyqtSlot(int)
    def rejection_slider_moved(self, value):
        self.settings_manager.change("rejection_threshold", value/10)

    @pyqtSlot(int)
    def slider0_moved(self, value):
        self.settings_manager.change("sd_weight", value/1000)

    @pyqtSlot(int)
    def slider1_moved(self, value):
        self.settings_manager.change("mean_weight", value/1000)

    @pyqtSlot(int)
    def slider2_moved(self, value):
        self.settings_manager.change("mode_weight", value/1000)

    @pyqtSlot(int)
    def slider3_moved(self, value):
        self.settings_manager.change("mode_count_weight", value/1000)

    @pyqtSlot(int)
    def slider4_moved(self, value):
        self.settings_manager.change("entropy_weight", value/1000)

