# atbp-lib
# The Interceptor is used to intercept and modify network packets.

import struct

from pydivert.windivert import *

from .protocol import GamePacket


class Interceptor:
    """
        Listens for network packets and calls a handler for each one.
    """
    
    DRIVER = "WinDivert.dll"
    
    GAME_PACKET_RULE = "tcp.DstPort == 9933 or tcp.SrcPort == 9933"
    GAME_PACKET_RULE_O = "outbound and tcp.DstPort == 9933"
    GAME_PACKET_RULE_I = "inbound and tcp.SrcPort == 9933"

    def __init__(self, packet_handler, rule):
        """
            Prepares the interceptor's settings.
        """
        
        self.packet_handler = packet_handler
        self.rule = rule
    
    def run(self):
        """
            Listens for packets matching the rule and handles them.
        """
        
        try:
            driver = WinDivert(self.DRIVER)
        except:
            print("---------------- ERROR ----------------")
            print("Failed to open {}. Make sure it's present in your working directory.".format(self.DRIVER))
            return
        with Handle(driver, filter=self.rule, priority=1000) as handle:
            while True:
                packet = handle.receive()
                new_packet = self.packet_handler(packet, handle)
                if new_packet is not None:
                    handle.send(new_packet)


class GameInterceptor(Interceptor):
    """
        Listens for game packets and breaks them down.
    """

    def __init__(self, game_packet_handler):
        """
            Prepares the interceptor's settings.
        """
        
        self.game_packet_handler = game_packet_handler
        self.leftover = None
        super().__init__(self.packet_handler, self.GAME_PACKET_RULE)
    
    def packet_handler(self, packet, handle):
        """
            Finds every game packet in the packet.
            Since game packets are sometimes grouped together, they need to be
            split up first. Sometimes, though, they'll be split out over
            multiple TCP packets, so we may need to reassemble them.
        """

        i = 0
        while i < len(packet.payload):
            # Check to see if it's a complete game packet.
            if packet.payload[i] == 0x80:
                if len(packet.payload) >= 3:
                    length = struct.unpack(">H", packet.payload[i + 1:i + 3])[0]
                    if len(packet.payload[i + 3:i + 3 + length]) == length:
                        game_packet = GamePacket(packet.payload[i:])
                        i += game_packet.length + 3
                        self.game_packet_handler(game_packet)
                    else:
                        self.leftover = packet.payload[i:]
                        break
                else:
                    self.leftover = packet.payload[i:]
                    break
            
            # Otherwise, try to reassemble it from the last packet.
            elif self.leftover and i == 0:
                reassembled_data = self.leftover + packet.payload
                game_packet = GamePacket(reassembled_data)
                i += game_packet.length + 3 - len(self.leftover)
                self.game_packet_handler(game_packet)
                self.leftover = None
            
            # Otherwise, this is an unknown packet.
            else:
                break
        
        return packet