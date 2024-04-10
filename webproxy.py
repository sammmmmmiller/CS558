# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:30:43 2024

@author: Sam
"""
from urllib.parse import urlparse
from socket import *
import sys
import logging

logging.basicConfig(level=logging.INFO)

if len(sys.argv) <= 1:
    logging.error('Usage: "python webproxy.py server_port"\n[server_port : port number of proxy server]')
    sys.exit(2)

try:
    port = int(sys.argv[1])
except ValueError:
    logging.error("Port number must be an integer.")
    sys.exit(2)

try:
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(('', port))
    tcpSerSock.listen(5)
    logging.info(f"Proxy Server running on port {port}...")
except Exception as e:
    logging.error(f"Failed to initialize server: {e}")
    sys.exit(2)

while True:
    try:
        tcpCliSock, addr = tcpSerSock.accept()
        logging.info(f'Received a connection from: {addr}')
    except Exception as e:
        logging.error(f"Error accepting connection: {e}")
        break

    try:
        message = tcpCliSock.recv(4096).decode('utf-8')
        message_lines = message.split('\n')
        method, full_url, version = message_lines[0].split(' ')
        parsed_url = urlparse(full_url)
        hostname = parsed_url.hostname
        path = parsed_url.path or '/'
        
        if method != 'GET':
            tcpCliSock.sendall(b"HTTP/1.0 501 Not Implemented\r\n\r\n")
            tcpCliSock.close()
        
        # for line in message_lines:
        #     if line.lower().startswith('host:'):
        #         host = line.split(': ')[1].strip()
        #         break

        destSock = socket(AF_INET, SOCK_STREAM)
        destSock.connect((hostname, 80))
        http_get_request = f"GET {path} HTTP/1.0\r\nHost: {hostname}\r\n\r\n"
        destSock.sendall(http_get_request.encode('utf-8'))
        
        response = b""
        while True:
            part = destSock.recv(4096)
            if not part: 
                break
            response += part
        
        tcpCliSock.sendall(response)
        
    except Exception as e:
        logging.error(f"Error handling request: {e}")
        
    finally:
        tcpCliSock.close()
        destSock.close()

tcpSerSock.close()
        
