#!/usr/bin/env python
import argparse

import sys
import itertools
import socket
import threading
import os
from socket import socket as Socket

HOST = socket.gethostbyname(socket.gethostname()) # The server's hostname or IP address
PORT = 1024  # The port used by the server

print(HOST)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"GET /index.html HTTP/1.1\r\nHost ip: local\r\nAccept: text/html\r\nConnection: close\r\n\r\n")
    data = s.recv(1024)

    while True:
        data = s.recv(1024)
        if not data:
            break
