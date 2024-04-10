# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:30:43 2024

@author: Sam
"""
from urllib.parse import urlparse
from socket import *
import sys

if len(sys.argv) <= 1:
    # print('Usage: "python webproxy.py server_port"\n[server_port : port number of proxy server]')
    sys.exit(2)

try:
    port = int(sys.argv[1])
except ValueError:
    # print("Port number must be an integer.")
    sys.exit(2)

try:
    proxySocket = socket(AF_INET, SOCK_STREAM)
    proxySocket.bind(('', port))
    proxySocket.listen(5)
    # print(f"Proxy Server running on port {port}...")
except Exception as e:
    # print(f"Failed to initialize server: {e}")
    sys.exit(2)

while True:
    try:
        clientSocket, addr = proxySocket.accept()
        # print(f'Received a connection from: {addr}')
    except Exception as e:
        # print(f"Error accepting connection: {e}")
        continue

    try:
        message = clientSocket.recv(4096).decode('utf-8')
        message_lines = message.split('\n')
        method, full_url, version = message_lines[0].split(' ')
        parsed_url = urlparse(full_url)
        hostname = parsed_url.hostname
        path = parsed_url.path or '/'
        
        if method != 'GET':
            clientSocket.sendall(b"HTTP/1.0 501 Not Implemented\r\n\r\n")
            clientSocket.close()
            continue
        
        # for line in message_lines:
        #     if line.lower().startswith('host:'):
        #         host = line.split(': ')[1].strip()
        #         break
    
        destinationSock = socket(AF_INET, SOCK_STREAM)
        destinationSock.connect((hostname, 80))
        http_get_request = f"GET {path} HTTP/1.0\r\nHost: {hostname}\r\n\r\n"
        destinationSock.sendall(http_get_request.encode('utf-8'))

        response = b""
        while True:
            part = destinationSock.recv(4096)
            if not part: 
                break
            response += part
        clientSocket.sendall(response)
        
    except Exception as e:
        # print(f"Error handling request: {e}")
        pass
        
    finally:
        clientSocket.close()
        destinationSock.close()

proxySocket.close()
        
