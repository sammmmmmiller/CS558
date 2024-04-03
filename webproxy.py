# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:30:43 2024

@author: Sam
"""

from socket import *
import sys
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

if len(sys.argv) <= 1:
    logging.error('Usage: "python ProxyServer.py server_port"\n[server_port : It is the Port Number Of Proxy Server]')
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
        continue

    try:
        message = tcpCliSock.recv(4096).decode('utf-8')
        message_lines = message.split('\n')
        
        url = ""
        host = ""    
        for line in message_lines:
            print(line)
            if line.startswith('GET'):
                url = line.split(' ')[1]
            elif line.lower().startswith('host:'):
                host = line.split(': ')[1].strip()
        print(url)
        print(host)
        if not url:
            logging.error("Received request without a URL.")
            tcpCliSock.close()
            continue
        
        destSock = socket(AF_INET, SOCK_STREAM)
        destSock.connect((host, 80))
        http_get_request = f"GET {url} HTTP/1.0\r\nHost: {host}\r\n\r\n"
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
        break
