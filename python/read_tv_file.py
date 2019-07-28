import json
from settings_store import texture_compatible
# read .tv file, condition data, throw Exception on error
def read_tv_file(filename, texture_names):
    with open(filename) as f:
        # read into tv_data
        tv_data = json.load(f)

        # ensure compatibility
        if not texture_compatible(texture_names, tv_data["texture_names"]):
            raise Exception("Data is not compatible.")

        # condition texture vectors by rounding and clipping them
        for textures in tv_data["texture_vectors"]:
            for i in range(len(textures)):
                textures[i] = min(round(textures[i]), 255)
        return tv_data

