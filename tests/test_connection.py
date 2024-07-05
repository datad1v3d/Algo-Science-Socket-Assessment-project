"""
This module test if the connections are working
"""
import unittest
import threading
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from my_server.server import FileHandler
from my_client import client

class TestServerClient(unittest.TestCase):
    """This is the class for testing server and client"""
    def setUp(self):
        """Start server in a separate thread"""
        server_thread = threading.Thread(target=FileHandler.server_program, args=(False,))
        server_thread.start()

    def test_server_program(self):
        """Start and immediately stop the server"""
        FileHandler.server_program(True)

    def test_client_program(self):
        """Run the client program"""
        client.client_program()

if __name__ == '__main__':
    unittest.main()
