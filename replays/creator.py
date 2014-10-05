# ATBP Tools
# Allows for the recording of replay files.

import os
import time

from data import *
from net.sniffer import *
from replays.replay import *


class ReplayCreator(GameSniffer):
    """
        Creates replays from sniffed packets.
    """
    
    def __init__(self):
        """
            Creates a new replay file for writing to.
        """

        super().__init__()        

        self.match_start = None
        self.replay_file = ReplayWriter(self.gen_replay_path())
        self.players = None

    def __del__(self):
        """
            Closes the replay file.
        """
        
        super().__del__()
        self.replay_file.close()
    
    def gen_replay_path(self):
        """
            Generates a new replay file path.
        """
        
        date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        return os.path.join(REPLAY_DIR, "replay_{}{}".format(date, REPLAY_EXT))
    
    def process_game_packet(self, timestamp, data):
        """
            Adds a new entry to the replay file.
        """
        
        if not self.match_start:
            # Check to see if this is the lobby initialized message.
            if data["a"] == 4:
                self.match_start = timestamp
            return
        
        # Make sure it is a cmd packet.
        if not data["a"] == 13 or not data["p"]["c"].startswith("cmd_"):
            return
        self.replay_file.write_action(timestamp - self.match_start, data["p"])