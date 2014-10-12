# atbp-lib
# Utilities for reading definition files.
# Definition files are XML files with various parameters which can be parsed.

import urllib.request
import xml.etree.ElementTree as ET

from ..data import *

URLS = get_data("urls")

def get_definition(name):
    """
        Fetches a definition file, parse it and return the XML root.
    """

    # Get the definitions file.
    try:
        definition_url = URLS["root"] + URLS["definitions"].format(name)
        definition_file = urllib.request.urlopen(definition_url)
        definition_data = definition_file.read().decode("utf-8")
    except urllib.error.URLError:
        print("Failed to fetch definition data: " + definition)
        return None

    # Parse it as an XML file.
    try:
        root = ET.fromstring(definition_data)
    except ET.ParseError:
        print("Failed to parse definition data: " + definition)
        return None

    return root