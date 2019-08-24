from os.path import join, expanduser
import json
from calc_tv import texture_names

# default path
default_settings_file = join(expanduser("~"), ".tv_threshold_settings")

# settings
def read_settings(settings_file):
    with open(settings_file) as f:
        settings = json.load(f)
        return settings

# compatibile if name sets match
def texture_compatible(names):
    try:
        if len(names) != len(texture_names):
            return False
        for name1, name2 in zip(names, texture_names):
            if name1 != name2:
                return False
        return True
    except Exception:
        return False

