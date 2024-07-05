'''server.py file contains the server script that binds a ports and responds to and 
unlimited amount of concurrent connections 
it gets the clients request (a string)
 and verifies if the string is contained in the file'''

import socket
import ssl
import threading
import time
from datetime import datetime
import re
import configparser
from typing import List, Tuple

class FileHandler:
    """
    the server program class to have an encapsulated the file handling logic 
    configuration variables reread_on_query and file_content in FileHandler class. 
    """
    def __init__(self):
        self.file_content: str = ""
        self.reread_on_query, self.ssl = self.config_opener('SETTINGS', 'reread_on_query', 'ssl')
        self.read_file()

    def config_opener(self, section: str, *keys: str) -> list[str]:
        '''Opens and ckecks for values within keys in config file'''
        config = configparser.ConfigParser()
         # Read the configuration file
        config.read('../config.ini')
        # Get the value from the configuration file
        return [config.get(section, key) for key in keys]
    
    def read_file(self) -> None:
        '''Reads the content of the file and stores it in self.file_content'''

        file_path = self.config_opener('PATH', 'linuxpath')[0]
        with open(file_path, 'r', encoding='utf-8') as file:
            self.file_content = file.readlines()

    def check_string_in_file(self, client_string: str) -> str:
        '''Verifies if the string input matches the content of the file'''
        try:
            if self.reread_on_query:
                self.read_file()

            # Check if the client string is in the file
            for line in self.file_content:
                line = line.rstrip('\x00')
                if re.search(client_string + '$', line):
                    return 'STRING EXISTS\n'
            return 'STRING NOT FOUND\n'
        except FileNotFoundError as e:
            return f'File not found: {str(e)}\n'
        except IOError as e:
            return f'Error reading file: {str(e)}\n'

    def handle_client(self, conn, address: Tuple[str, int]) -> None:
        '''Handles connections from the client'''
        print("Connection from:", address)
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"DEBUG: From connected user ({address}): {data}")
                start_time = time.time()
                response = self.check_string_in_file(data)
                conn.send(response.encode())
                execution_time = time.time() - start_time
                print(f"DEBUG: Execution time: {execution_time} seconds  Time: {datetime.now()}")
            except UnicodeDecodeError as e:
                print(f'Error decoding client data: {str(e)}')
                break
            except (socket.error, socket.timeout) as e:
                print(f'Socket error: {str(e)}')
                break
        conn.close()
        print("Client disconnected:", address)

    def server_program(self, run_forever: bool = True) -> None:
        '''Sets up a server to handle client connections'''
            # Get the hostname
        host = socket.gethostname()
        port = 5000  # Initiate port

        server_socket = socket.socket()  # Get instance


        if self.ssl:
            # Create a default SSL context with client authentication enabled
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            # Load the server's self-signed certificate and private key into the SSL context
            try:
                ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')
            except FileNotFoundError as e:
                print(f'Error loading certificate files: {str(e)}')
                return
                # Wrap server_socket with SSL
            try:
                server_socket = ssl_context.wrap_socket(server_socket, server_side=True)
                server_socket.bind((host, port))
            except ssl.SSLError as e:
                print(f'Error wrapping socket with SSL: {str(e)}')
                return
        else:
            server_socket.bind((host, port))

        # Configure how many clients the server can listen to simultaneously
        server_socket.listen(5)

        print("Server started on port:", port)

        while run_forever:
            # Accept new connection
            try:
                conn, address = server_socket.accept()
            except socket.error as e:
                print(f'Socket error accepting connection: {str(e)}')
                continue
            # Create a new thread for each client
            client_thread = threading.Thread(target=self.handle_client, args=(conn, address))
            client_thread.start()  # Start the thread

        server_socket.close()  # Close the server socket (not reached in practice)

if __name__ == '__main__':
    file_handler = FileHandler()
    file_handler.server_program()
