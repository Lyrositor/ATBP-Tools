# ATBP Tools
# Allows for the recording of replay files.

import yaml

from net.sniffer import *

class ReplayCreator(GameSniffer):
    """
        Creates replays from sniffed packets.
    """
    
    def process_game_packet(self, timestamp, packet):
        """
            Adds a new entry to the replay file.
        """
        
        print("{}: {}".format(time.strftime("%H:%M:%S", time.localtime(timestamp)), packet.data))