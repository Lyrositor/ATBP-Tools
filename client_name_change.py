#!/usr/bin/env python3
# ATBP Tools - Client Name Change
# Changes the client's name when connecting.
# DO NOT USE in online play, unless you want to risk getting caught and banned.

from net.packets import *
from net.interceptor import *

NAME = ""

def reroute_packet(packet):
    """
        Reroutes the matched packet.
    """
    
    if packet.payload:
        try:
            atbp_packet = ATBPPacket(packet.payload)
        except ValueError:
            return packet
        d = atbp_packet.data.value
        if d["a"].value == 1:
            d["p"]["p"]["name"].value = NAME
            packet.payload = atbp_packet.get_raw_packet()
    return packet

def main():
    """
        Listens for the name submission packet, then modify it.
    """
    
    global NAME
    
    NAME = input("Please input your desired display name: ")
    
    # Start the interceptor.
    interceptor = Interceptor(reroute_packet)
    print("Running...")
    try:
        interceptor.run()
    except KeyboardInterrupt:
        print("\r    ")

    # Wait for the user to exit.
    print("Complete.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()