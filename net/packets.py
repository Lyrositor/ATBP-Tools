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


class ATBPVar:
    """
        Represents a variable for an ATBPPacket.
    """
    
    BOOL = 0x1
    CHAR = 0x2
    SHORT = 0x3
    LONG = 0x4
    FLOAT = 0x6
    DOUBLE = 0x7
    STRING = 0x8
    LIST = 0x11
    DICTIONARY = 0x12
    
    def __init__(self, s):
        """
            Loads the next variable from the provided stream.
        """
    
        self.value = None
        self.type = None
        self.value, self.type = self.read(s)
    
    def __repr__(self):
        """
            Display the variable's value.
        """
        
        return repr(self.value)

    def __getitem__(self, key):
        """
            If the value is a dictionary or a list, return that value.
        """
        
        return self.value[key]
        
    def read(self, s, var_type=None):
        """
            Reads the variable from a stream.
        """

        if var_type is None:
            var_type = struct.unpack(">B", s.read(1))[0]

        value = None
        if var_type == self.BOOL:
            value = struct.unpack(">?", s.read(1))[0]
        elif var_type == self.CHAR:
            value = struct.unpack(">B", s.read(1))[0]
        elif var_type == self.SHORT:
            value = struct.unpack(">h", s.read(2))[0]
        elif var_type == self.LONG:
            value = struct.unpack(">i", s.read(4))[0]
        elif var_type == self.FLOAT:
            value = struct.unpack(">f", s.read(4))[0]
        elif var_type == self.DOUBLE:
            value = struct.unpack(">d", s.read(8))[0]
        elif var_type == self.STRING:
            l = struct.unpack(">H", s.read(2))[0]
            value = s.read(l).decode("ascii")
        elif var_type == self.LIST:
            l = struct.unpack(">H", s.read(2))[0]
            value = []
            for i in range(l):
                value.append(ATBPVar(s))
        elif var_type == self.DICTIONARY:
            l = struct.unpack(">H", s.read(2))[0]
            value = {}
            for i in range(l):
                name = self.read(s, self.STRING)[0]
                value[name] = ATBPVar(s)

        return value, var_type

    def get_raw(self):
        """
            Gets the raw version of the var.
        """
        
        value = bytes()
        if self.type == self.BOOL:
            value = struct.pack(">B?", self.type, self.value)
        elif self.type == self.CHAR:
            value = struct.pack(">BB", self.type, self.value)
        elif self.type == self.SHORT:
            value = struct.pack(">Bh", self.type, self.value)
        elif self.type == self.LONG:
            value = struct.pack(">Bi", self.type, self.value)
        elif self.type == self.FLOAT:
            value = struct.pack(">Bf", self.type, self.value)
        elif self.type == self.DOUBLE:
            value = struct.pack(">Bd", self.type, self.value)
        elif self.type == self.STRING:
            value = struct.pack(">BH", self.type, len(self.value))
            value += self.value.encode("ascii")
        elif self.type == self.LIST:
            value = struct.pack(">BH", self.type, len(self.value))
            for v in self.value:
                value += v.get_raw()
        elif self.type == self.DICTIONARY:
            value = struct.pack(">BH", self.type, len(self.value))
            for name, v in self.value.items():
                value += struct.pack(">H", len(name))
                value += name.encode("ascii")
                value += v.get_raw()
        return value


class ATBPPacket:

    HEADER = 0x80

    def __init__(self, data):
        """
            Initializes the packet.
        """

        self.header, length = struct.unpack(">BH", data[:3])
        if self.header != self.HEADER:
            raise ValueError
        self.data = ATBPVar(io.BytesIO(data[3:]))
        
    def get_raw_packet(self):
        """
            Returns the raw packet version.
        """
        
        payload = self.data.get_raw()
        stream = io.BytesIO()
        stream.write(struct.pack(">BH", self.HEADER, len(payload)))
        stream.write(payload)
        return stream.getvalue()