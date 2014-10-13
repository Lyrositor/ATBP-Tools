#!/usr/bin/env python3
# Base Interceptor
# Use as a base for intercepting game packets.

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

def start_interceptor():
    interceptor = GameInterceptor(packet_handler)
    try:
        interceptor.run()
    except KeyboardInterrupt:
        pass

def main():   
    try:
        start_interceptor()
    except:
        traceback.print_exc()
    finally:
        input("Press Enter to exit.")

if __name__ == "__main__":
    main()