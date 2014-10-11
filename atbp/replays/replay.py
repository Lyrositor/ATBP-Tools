# atbp-lib
# Replay file tools.

import yaml

from ..net.protocol import GamePacketVar

def var_representer(dumper, data):
    """
        YAML Representer for the GamePacketVar class.
    """

    return dumper.represent_sequence("!V", [data.v, data.t])

yaml.add_representer(GamePacketVar, var_representer)

    
class Replay:
    """
        Represents a replay. Allows for the reading and writing of replays.
    """
    
    FILE_EXT = ".atbp"

    def __init__(self, entries=[], path=None, simple=False):
        """
            Create a new replay, optionally with initial data.
            If path is specified, entries will be written to the file as they
            are added.
            If simple is specified, the replay output will be simplified.
        """
        
        self.entries = entries
        self.replay_file = None
        if path:
            self.replay_file = open(path, "w")
        self.simple = simple

    def __del__(self):
        """
            Closes any opened replay file.
        """
        
        if self.replay_file:
            self.replay_file.close()

    def add_entry(self, timestamp, data):
        """
            Adds a new entry to the list of entries.
        """

        if self.simple:
            if data["a"] != 0xD or data["p"]["c"][:3] != "cmd":
                return
            entry = {
                "name": data["p"]["c"].v,
                "params": data["p"]["p"].to_normal(),
                "time": timestamp
            }
        else:
            entry = {"time": timestamp, "data": data}
        self.entries.append(entry)
        if self.replay_file:
            yaml.dump(entry, self.replay_file, explicit_start=True)
            self.replay_file.flush()

    def save_to_file(self, file_path):
        """
            Saves the replay data to a YAML file.
        """
        
        with open(file_path, "w") as f:
            yaml.dump_all(self.entries, f, explicit_start=True)
    
    def from_file(file_path):
        """
            Loads a replay from the specified path.
        """
        
        with open(file_path, "r") as f:
            entries = yaml.load_all(f.read())
        return Replay(entries)