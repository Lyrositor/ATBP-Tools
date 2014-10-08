# ATBP Tools
# Server-side utilities.

from socketserver import TCPServer

from data import *
from .packets import *


class GameServer(TCPServer):
    """
        Emulates an ATBP game server.
    """
    
    def __init__(self, packet_handler):
        """
            Create the server.
        """
        
        super().__init__(("localhost", PORT), packet_handler)
    
    def intercept_forever(self):
        """
            Intercepts connections made to the actual game server and redirects them here.
        """