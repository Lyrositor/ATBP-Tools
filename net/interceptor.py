#!/usr/bin/env python3
# ATBP Tools
# Tools for intercepting game packets and modifying them.

from .packets import *
from pydivert.windivert import *


class Interceptor:
    """
        Intercepts game packets.
    """
    
    GAME_PACKET_RULE = "outbound and tcp.DstPort == 9933"
    
    def __init__(self, packet_handler):
        """
            Prepares the interceptor's settings.
        """
        
        self.packet_handler = packet_handler

    def run(self):
        """
            Listens for packets matching the rule and handles them.
        """
        
        driver = WinDivert(r"DLLs\WinDivert.dll")
        with Handle(driver, filter=self.GAME_PACKET_RULE, priority=1000) as handle:
            while True:
                packet = handle.receive()
                new_packet = self.packet_handler(packet)
                handle.send(new_packet)
