#!/usr/bin/env python3
# Base Interceptor
# Use as a base for intercepting game packets.

import sys
sys.path.append("..")

import traceback

from atbp.net.interceptor import GameInterceptor
from atbp.net.protocol import GamePacket


def packet_handler(game_packet):
    """
        Do something.
    """
    
    pass
    
    #########################
    # Write your code here. #
    #########################

    return packet

def main():   
    interceptor = GameInterceptor(packet_handler)
    try:
        interceptor.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit.")