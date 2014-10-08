#!/usr/bin/env python3
# ATBP Tools - Client Redirect
# Intercepts game packets from the client and reroutes them to another server.

from net.interceptor import *

IP = "192.168.1.0"

def reroute_packet(packet):
    """
        Reroutes the matched packet.
    """
    
    packet.dst_addr = IP
    return packet

def main():
    """
        Listens for outgoing game network data and reroutes it.
    """

    global IP
    
    IP = input("Please enter your IP: ")
    
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