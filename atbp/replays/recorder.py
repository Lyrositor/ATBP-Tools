# atbp-lib
# Tools for recording a new replay.

import time

from ..net.interceptor import GameInterceptor
from .replay import Replay


class ReplayRecorder(GameInterceptor):
    """
        Records game packets as they pass.
    """
    
    def __init__(self, replay_path, simple=False):
        """
            Creates a new replay file for writing to.
            If 'simple' is True, the replay will contain only cmd entries and
            will be easier to read.
        """

        super().__init__(self.process_packet)

        self.match_start = None
        self.replay = Replay(path=replay_path, simple=simple)

    def process_packet(self, game_packet):
        """
            Process a packet which matched the rule.
        """
        
        data = game_packet.data

        if not self.match_start:
            # Check to see if this is the first relevant message.
            if data["a"] != 0:
                return
            print("Match started. Now recording.")
            self.match_start = time.time()
            self.replay.entries = []

        self.replay.add_entry(time.time() - self.match_start, data)