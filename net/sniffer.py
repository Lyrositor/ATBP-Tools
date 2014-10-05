# ATBP Tools
# Simple network sniffer for IP packets.

from ctypes import *
import socket
import sys
import time

from .packets import *
from .winpcapy import *


class GameSniffer:
    """
        Sniffs the network for game packets.
    """

    def __init__(self):
        """
            Initializes the sniffing socket.
        """
        
        PHAND = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(pcap_pkthdr), POINTER(c_ubyte))
        self.packet_handler = PHAND(self._packet_handler)
        alldevs = POINTER(pcap_if_t)()
        errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
        
        # Retrieve the device list.
        if pcap_findalldevs(byref(alldevs), errbuf) == -1:
            print("Failed to find all devices: %s\n" % errbuf.value)
            sys.exit(1)
        try:
            d = alldevs.contents
        except:
            print("Failed to find all devices: make sure you have admin privileges.")
            sys.exit(1)
        
        # Prompt the user for the device he wishes to listen on.
        i = 0
        while d:
            i += 1
            print("{}. {} ({})".format(
                i,
                d.name.decode("ascii"),
                d.description.decode("ascii") if d.description else "[No description available.]"
            ))
            if d.next:
                d = d.next.contents
            else:
                d = None
        if i is 0:
            print("No interfaces found. Make sure WinPcap is installed.")
            sys.exit(1)
        dev_num = None
        while dev_num is None:
            try:
                n = int(input("Please enter the ID of the device you wish to listen on: "))
            except ValueError:
                print("Invalid value. Please try again.")
                continue
            if n < 1 or n > i:
                print("Value is out of range. Please try again.")
                continue
            dev_num = n
        
        # Prepare the device for listening.
        d = alldevs
        for i in range(dev_num - 1):
            d = d.contents.next
        d = d.contents
        self.adhandle = pcap_open_live(d.name, 65536, 1, 1000, errbuf)
        if not self.adhandle:
            print("Unable to open adapter. {} is not supported by Pcap-WinPcap.".format(d.contents.name.decode("ascii")))
            pcap_freealldevs(alldevs)
            sys.exit(1)
        pcap_freealldevs(alldevs)

    def __del__(self):
        """
            Closes the socket before being destroyed.
        """
        
        pcap_close(self.adhandle)

    def run(self):
        """
            Runs the main sniffing loop.
        """
        
        pcap_loop(self.adhandle, -1, self.packet_handler, None)
        
    def _packet_handler(self, param, header, pkt_data):
        """
            Called when a packet has been received.
        """
        
        try:
            packet = IPPacket(bytes(pkt_data[0xE:header.contents.len]))
            if packet.tcp and packet.tcp.atbp:
                self.process_game_packet(header.contents.ts.tv_sec, packet.tcp.atbp.data)
        except ValueError:
            # Not a valid IPv4 packet. Ignore it.
            pass
    
    def process_game_packet(self, timestamp, data):
        """
            Processes a sniffed game packet. Implement this in a subclass.
        """