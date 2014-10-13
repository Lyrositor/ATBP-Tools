# atbp-lib
# Utilities for reading data from the data files.

import os.path
import sys

DATA_DIR = os.path.join("atbp", "data")

def get_data(name):
    """
        Reads the data contained in a data file.
        
        A data file is a newline-separated list of entries, optionally with
        comments. Entries can optionally have a space-separated value.
        Order is not preserved when loading.
    """

    try:
        data = {}
        with open(os.path.join(DATA_DIR, name + ".txt")) as f:
            for line in f.readlines():
                # Read the line's information.
                l = line.strip()
                if len(l) == 0 or l[0] == "#":
                    continue
                e = l.split(" ", 1)
                
                # Store the data.
                name = e[0]
                value = None
                if len(e) == 2:
                    v = e[1].strip()
                    try:
                        value = int(v)
                    except ValueError:
                        try:
                            value = int(v, 16)
                        except ValueError:
                            value = v
                data[name] = value

        return data
    except (OSError, IOError):
        return None