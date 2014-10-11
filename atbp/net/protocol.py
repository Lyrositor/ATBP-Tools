# atbp-lib
# Contains definitions for the ATBP network protocol.

import io
import struct

from ..data import *

D = get_data("net")


class GamePacket:
    """
        The ATBP game packet, a simple, unencrypted dictionary of data.
    """

    HEADER = 0x80

    def __init__(self, data):
        """
            Initializes the packet.
        """

        if len(data) < 3:
            raise ValueError
        self.header, self.length = struct.unpack(">BH", data[:3])
        if self.header != self.HEADER:
            raise ValueError
        self.data = GamePacketVar(io.BytesIO(data[3:3 + self.length]))
        
    def get_raw_packet(self):
        """
            Returns the raw packet version.
        """
        
        payload = self.data.get_raw()
        data = struct.pack(">BH", self.header, len(payload)) + payload
        return data


class GamePacketVar:
    """
        Represents a variable for an ATBPPacket.
    """
    
    def __init__(self, s):
        """
            Loads the next variable from the provided stream.
        """
    
        self.v, self.t = self.read(s)
    
    def __repr__(self):
        """
            Return the variable's value.
        """
        
        return repr(self.v)

    def __str__(self):
        """
            Return the variable's string conversion.
        """
        
        return str(self.v)

    def __getitem__(self, key):
        """
            If the value is a dictionary or a list, return that value.
        """
        
        return self.v[key]
    
    def __eq__(self, other):
        """
            Checks if the stored value equals other.
        """
        
        return self.v == other
    
    def __ne__(self, other):
        """
            Checks if the stored value is not equal to other.
        """
        
        return self.v != other

    def to_normal(self):
        """
            Gives a normal representation of the var.
        """
        
        if isinstance(self.v, list):
            return [v.to_normal() for v in self.v]
        elif isinstance(self.v, dict):
            return {k: v.to_normal() for k, v in self.v.items()}
        else:
            return self.v
    
    def read(self, s, var_type=None):
        """
            Reads the variable from a stream.
        """

        if var_type is None:
            var_type = struct.unpack(">B", s.read(1))[0]

        value = None
        if var_type == D["vars.bool"]:
            value = struct.unpack(">?", s.read(1))[0]
        elif var_type == D["vars.char"]:
            value = struct.unpack(">B", s.read(1))[0]
        elif var_type == D["vars.short"]:
            value = struct.unpack(">h", s.read(2))[0]
        elif var_type == D["vars.long"]:
            value = struct.unpack(">i", s.read(4))[0]
        elif var_type == D["vars.float"]:
            value = struct.unpack(">f", s.read(4))[0]
        elif var_type == D["vars.double"]:
            value = struct.unpack(">d", s.read(8))[0]
        elif var_type == D["vars.string"]:
            l = struct.unpack(">H", s.read(2))[0]
            value = s.read(l).decode("ascii")
        elif var_type == D["vars.list"]:
            l = struct.unpack(">H", s.read(2))[0]
            value = []
            for i in range(l):
                value.append(GamePacketVar(s))
        elif var_type == D["vars.dictionary"]:
            l = struct.unpack(">H", s.read(2))[0]
            value = {}
            for i in range(l):
                name = self.read(s, D["vars.string"])[0]
                value[name] = GamePacketVar(s)

        return value, var_type

    def get_raw(self):
        """
            Gets the raw version of the var.
        """
        
        value = bytes()

        if self.t == D["vars.bool"]:
            value = struct.pack(">B?", self.t, self.v)
        elif self.t == D["vars.char"]:
            value = struct.pack(">BB", self.t, self.v)
        elif self.t == D["vars.short"]:
            value = struct.pack(">Bh", self.t, self.v)
        elif self.t == D["vars.long"]:
            value = struct.pack(">Bi", self.t, self.v)
        elif self.t == D["vars.float"]:
            value = struct.pack(">Bf", self.t, self.v)
        elif self.t == D["vars.double"]:
            value = struct.pack(">Bd", self.t, self.v)
        elif self.t == D["vars.string"]:
            value = struct.pack(">BH", self.t, len(self.v))
            value += self.v.encode("ascii")
        elif self.t == D["vars.list"]:
            value = struct.pack(">BH", self.t, len(self.v))
            for v in self.v:
                value += v.get_raw()
        elif self.t == D["vars.dictionary"]:
            value = struct.pack(">BH", self.t, len(self.v))
            for name, v in self.v.items():
                value += struct.pack(">H", len(name))
                value += name.encode("ascii")
                value += v.get_raw()

        return value