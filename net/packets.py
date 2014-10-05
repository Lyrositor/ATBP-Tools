# ATBP Tools
# Contains definitions for various protocols' packets.

import io
import socket
import struct

from data import *


class IPPacket:
    """
        Creates an IP packet from a bytes object.
    """
    
    def __init__(self, data):
        """
            Initializes the packet.
        """

        header = struct.unpack(">BBHHHBBH4s4s", data[:20])
        
        # Check that the packet is IPv4.
        self.version = header[0] >> 4
        self.ihl = header[0] & 0xF
        header_length = self.ihl * 4
        if self.version != 4:
            raise ValueError
            
        # Get packet's properties.
        self.ttl = header[5]
        self.protocol = header[6]
        self.src_address = socket.inet_ntoa(header[8])
        self.dst_address = socket.inet_ntoa(header[9])
        
        # Create the encapsulated TCP packet, if applicable.
        self.data = data[header_length:]
        self.tcp = None
        if self.protocol == TCPPacket.PROTOCOL_ID:
            self.tcp = TCPPacket(self.data)

        
class TCPPacket:
    """
        Creates a TCP packet from a bytes object.
    """
    
    PROTOCOL_ID = 0x06
    
    def __init__(self, data):
        """
            Initializes the packet.
        """
        
        header = struct.unpack(">HHLLBBHHH" , data[:20])
        
        # Get packet's properties.
        self.src_port = header[0]
        self.dst_port = header[1]
        self.sequence = header[2]
        self.acknowledgement = header[3]
        
        # Get the data.
        self.data_offset = header[4] >> 4
        header_length = self.data_offset * 4
        self.data = data[header_length:]
        
        # Create the encapsulated ATBP packet, if applicable.
        self.atbp = None
        if GAME_PORT in (self.src_port, self.dst_port) and self.data and self.data[0] == ATBPPacket.HEADER:
            self.atbp = ATBPPacket(self.data)


class Vars:
    """
        Lists variable types.
    """
    
    BOOL = 0x1
    CHAR = 0x2
    SHORT = 0x3
    INTEGER = 0x4
    FLOAT = 0x6
    DOUBLE = 0x7
    STRING = 0x8
    LIST = 0x11
    DICTIONARY = 0x12


class ATBPPacket:

    HEADER = 0x80

    def __init__(self, data):
        """
            Initializes the packet.
        """

        self.header, length = struct.unpack(">Bh", data[:3])
        self.data = self.read_var(io.BytesIO(data[3:]))
        
    def read_var(self, s, var_type=None):
        """
            Reads a variable from a stream.
        """

        if var_type is None:
            var_type = struct.unpack(">B", s.read(1))[0]

        if var_type == Vars.BOOL:
            return struct.unpack(">?", s.read(1))[0]
        elif var_type == Vars.CHAR:
            return struct.unpack(">b", s.read(1))[0]
        elif var_type == Vars.SHORT:
            return struct.unpack(">h", s.read(2))[0]
        elif var_type == Vars.INTEGER:
            return struct.unpack(">i", s.read(4))[0]
        elif var_type == Vars.FLOAT:
            return struct.unpack(">f", s.read(4))[0]
        elif var_type == Vars.DOUBLE:
            return struct.unpack(">d", s.read(8))[0]
        elif var_type == Vars.STRING:
            l = struct.unpack(">H", s.read(2))[0]
            return s.read(l).decode("ascii")
        elif var_type == Vars.LIST:
            l = struct.unpack(">H", s.read(2))[0]
            _list = []
            for i in range(l):
                _list.append(self.read_var(s))
            return _list
        elif var_type == Vars.DICTIONARY:
            l = struct.unpack(">H", s.read(2))[0]
            dictionary = {}
            for i in range(l):
                name = self.read_var(s, Vars.STRING)
                dictionary[name] = self.read_var(s)
            return dictionary

        return None