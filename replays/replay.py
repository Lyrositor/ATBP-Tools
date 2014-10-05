# ATBP Tools
# Representation for replay files.

import yaml


class ReplayWriter:
    """
        Replay file writing class.
    """

    def __init__(self, path):
        """
            Opens the file for writing.
        """
        
        self.f = open(path, "w")

    def close(self):
        """
            Closes the file.
        """
        
        self.f.close()

    def write_action(self, timestamp, action):
        """
            Formats the action to the YAML format and writes it out.
        """
        
        data = [{
            "time": timestamp,
            "name": action["c"],
            "params": action["p"]
        }]
        yaml.dump(data, self.f, indent=2, default_flow_style=False)
        self.f.flush()