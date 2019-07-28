from os.path import join, expanduser
import json

# default path
default_settings_file = join(expanduser("~"), ".tv_threshold_settings")

# settings
def read_settings(settings_file):
    with open(settings_file) as f:
        settings = json.load(f)
        return settings

# compatibile if name sets match
def texture_compatible(names1, names2):
    try:
        if len(names1) != len(names2):
            return False
        for name1, name2 in zip(names1, names2):
            if name1 != name2:
                return False
        return True
    except Exception:
        return False

