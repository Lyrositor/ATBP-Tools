# ATBP Tools
# Provides access to the data files.

import os

from .constants import *

DATA_DIR = "data"

def read_list_file(name):
    """
        Reads the data from a list file.
        
        A list file is a newline-seperated list of entries, optionally with
        comments.
    """

    try:
        data = []
        with open(os.path.join(DATA_DIR, name + ".txt")) as f:
            for line in f.readlines():
                l = line.strip()
                if len(l) == 0 or l[0] == "#":
                    continue
                data.append(line.strip())
        return data
    except (OSError, IOError):
        return None