# ATBP Tools
# Downloads definitions and sound files.

import os
import urllib.request
import xml.etree.ElementTree as ET

from data import *

def get_sounds_list(definitions):
    """
        Fetches a list of sounds from the game server.
    """

    sounds_list = []

    # Fetch every definition file and parse it for sound objects.
    for definition in definitions:
        print("Processing " + definition)

        # Get the definitions file.
        try:
            definition_data = urllib.request.urlopen(DEFINITIONS_URL.format(definition)).read().decode("utf-8")
        except urllib.error.URLError:
            print("Failed to fetch definition data: " + definition)
            continue
        with open("definitions/{}.xml".format(definition), "w") as f:
             f.write(definition_data)
        # Parse it as an XML file.
        try:
            root = ET.fromstring(definition_data)
        except ET.ParseError:
            print("Failed to parse definition data: " + definition)
            continue

        # Load the list of sounds.
        for soundObjects in root.iter("soundObjects"):
            for String in soundObjects.iter("String"):
                sounds_list.append(String.text)

    return sounds_list

def download_sounds(sounds_list, output_dir):
    """
        Downloads every file in the list and saves them.
    """

    for sound in sorted(sounds_list):
        url = SOUNDS_URL.format(sound)
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