# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:30:43 2024

@author: Sam
"""

from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', int(sys.argv[2])))
tcpSerSock.listen(5)

while 1:
    tcpCliSock, addr = tcpSerSock.accept()
    message = tcpCliSock.recv(4096).decode('utf-8')
    message_lines = message.split('\n')
    print('Received a connection from:', addr)
    print(message_lines)

    url = ""
    host = ""    
    for line in message_lines:
        if line.startswith('GET'):
            url = line.split(' ')[1]
        elif line.lower().startswith('host:'):
            host = line.split(': ')[1].strip()
    
    if len(url) == 0:
        raise NotImplementedError()
        
    destSock = socket(AF_INET, SOCK_STREAM)
    destSock.connect((host, 80))
    http_get_request = f"GET {url} HTTP/1.0\nHost: {host}\n\n"
    destSock.sendall(http_get_request.encode('utf-8'))

    response = b""
    while 1:
        part = destSock.recv(4096)
        if not part: break
        response += part
    tcpCliSock.sendall(response)

    tcpCliSock.close()
    destSock.close()
    