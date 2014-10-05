# ATBP Tools
# Representation for replay files.

import yaml


class ReplayWriter:
    """
        Replay file writing class.
    """
    
    FILE_EXT = ".atbp"

    def __init__(self, path):
        """
            Opens the file for writing.
        """
        
        self.f = open(path, "w")
    
    def write_action(self, action):
        """
            Formats the action to the YAML format and writes it out.
        """
        
        yaml.dump({}, self.f, indent=2, default_flow_style=False)