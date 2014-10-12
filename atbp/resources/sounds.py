# atbp-lib
# Utilies for listing files and downloading them.

import urllib.request

from ..data import *
from .definitions import *

DEFINITIONS = get_data("definitions")
OTHER_SOUNDS = get_data("other_sounds")
URLS = get_data("urls")

def get_all_sounds():
    """
        Fetches a list of all known sounds from definition files.
    """

    sounds_list = []
    for definition in sorted(DEFINITIONS):
        print("Processing " + definition)
        data = get_definition(definition)
        if not data:
            continue

        # Load the list of sounds.
        for soundObjects in data.iter("soundObjects"):
            for String in soundObjects.iter("String"):
                sounds_list.append(String.text)

    sounds_list.extend(OTHER_SOUNDS)

    return set(sounds_list)

def download_sounds(sounds_list, output_dir):
    """
        Downloads every file in the list and saves them.
    """

    for sound in sorted(sounds_list):
        url = URLS["root"] + URLS["sounds"].format(sound)
        print("Downloading " + url)

        # Get the file data.
        try:
            data = urllib.request.urlopen(url).read()
        except urllib.error.URLError:
            print("Failed to fetch sound file: " + sound)
            continue

        # Save the data to a file.
        path = os.path.join(output_dir, sound + ".ogg")
        try:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with open(path, "wb") as f:
                f.write(data)
        except (IOError, OSError):
            print("Failed to write sound file: " + path)
            continue