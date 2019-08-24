
"""Settings are kept in the user's home directory in
file .tv_threshold_settings.  Access them using this manager.

Provides the following services:
  Global variables, do not directly change their values.
     settings - the active settings
     default_settings
  Note: settings is global and also signal_settings_changed provides settings.

  Class SettingsManager, provides methods to safely change and notify settings:
     copy() - get your copy of settings
     change(provided settings) - change provided settings values, signal change
     _load(), load_from() - change all settings values from file, signal change
     _save(), save_to(fname), save settings to user default file or named file

Usage:
  Use SettingsManager to initialize or modify the global settings variable.
  SettingsManager is a singleton because it manages the settings resource.
  Instantiate SettingsManager before relying on settings values.
  Listen to the signal_settings_changed signal if you need to respond to change.
  Access the settings global variable without needing SettingsManager.
"""
from os.path import expanduser
import os
import json
from copy import deepcopy
from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSignal, pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt
from show_popup import show_popup
from settings_store import default_settings_file

# default
default_settings = {"rejection_threshold":50,
                    "sd_weight":0.5, "mean_weight":0.5, "mode_weight":0.0,
                    "mode_count_weight":0.5, "entropy_weight":0.5}

settings = deepcopy(default_settings)

# SettingsManager provides services to manage the global settings variable
# and to signal change.  Do not modify settings directly.
class SettingsManager(QObject):

    # signal
    signal_settings_changed = pyqtSignal(dict, name='settingsChanged')

    def __init__(self):
        super(SettingsManager, self).__init__()

        # load default settings
        if os.path.exists(default_settings_file):
            self._load()
        else:
            self.change_all(default_settings)

    # get a copy of settings to protect the original
    def copy(self):
        return deepcopy(settings)

    # change provided settings
    def change(self, name, value):
        global settings
        settings[name] = value

        # signal change
        self.signal_settings_changed.emit(settings)

        # save settings in user store
        self._save()

    def change_all(self, new_settings):
        global settings
        for name,value in new_settings.items():
            settings[name]=value

        # signal change
        self.signal_settings_changed.emit(settings)

        # save settings in user store
        self._save()

    def save_to(self, filename):

        # export settings in JSON
        try:
            with open(filename, "w") as f:
                json.dump(settings, f)
        except Exception as e:
            show_popup(None, "Error saving settings file: %s" % str(e))

    def _save(self):
        self.save_to(default_settings_file)

    def load_from(self, filename):
        try:
            with open(filename) as f:
                new_settings = json.load(f)
                if settings.keys() != new_settings.keys():
                    raise Exception("Incompatible settings file.")
                settings = deepcopy(new_settings)

        except Exception as e:
            if filename == default_settings_file:
                self._save()
            else:
                show_popup(None, "Error reading settings file: %s"%str(e))

    def _load(self):
        self.load_from(default_settings_file)

