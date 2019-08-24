import json
from settings_store import texture_compatible
# read .tv file, condition data, throw Exception on error
def read_tv_file(filename):
    with open(filename) as f:
        # read into tv_data
        tv_data = json.load(f)

        # ensure compatibility
        if not texture_compatible(tv_data["texture_names"]):
            raise Exception("Data is not compatible.")

        return tv_data

