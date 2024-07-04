'''
client.py script that connects to a server 
takes and display input from the user and sends it to the server
recieves and display the output from the server
'''
import socket
import ssl
import configparser
from typing import Any

def config_opener(section: str, key: str) -> Any:
    '''Opens and checks for values within keys in the config file'''
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config.getboolean(section, key)

def client_program() -> None:
    '''
    This function sets up a client to connect to a server over SSL
    using a self signed certificate for server authentication.
    '''
    try:
        host = socket.gethostname()  # get the hostname this wont work if not same pc
        port = 5000  # socket server port number

        client_socket = socket.socket()  # instantiate
        using_ssl = config_opener('SETTINGS', 'ssl')
        if using_ssl:
            # create a default ssl context
            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ssl_context.load_verify_locations(cafile='../my_server/server.crt')
            conn = ssl_context.wrap_socket(client_socket, server_side=False, server_hostname=host)
        else:
            conn = client_socket  # Use the regular socket without SSL/TLS

        conn.connect((host, port))  # connect to the server

        message = input(" -> ")  # take input

        while message.lower().strip() != 'bye':
            conn.send(message.encode())  # send message
            data = conn.recv(1024).decode()  # receive response

            print('Received from server: ' + data)  # show in terminal

            message = input(" -> ")  # again take input

        client_socket.close()  # close the connection
    except Exception as e:
        print(f'Error in client program: {str(e)}')


if __name__ == '__main__':
    client_program()
