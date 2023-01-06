#!/usr/bin/env python3

import argparse
import socket
import sys
import itertools
import webbrowser
import os
from _thread import *
import threading


from socket import socket as Socket

# A simple web server

SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=1024, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((SERVER, args.port))
        server_socket.listen(1)

        print(f"Server Ready:")

        index = 0
        while True:

           
            conn, addr = server_socket.accept()
                
            # insert thread lock here
            client_thread = threading.Thread(target=clientThreads, args=(conn, addr))
            client_thread.start()

            s = "Thread number: "
            print(f"{s}{index}")
            index += 1
                
                

    return 0


def http_handle(request_string):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    
    data = 'HTTP/1.1 200 OK\r\n'
    data+= 'Connection: keep-alive\r\n'
    data+= 'Content-Type: text/html; encoding=utf-8\r\n'
    f = open('index.html', 'r')
    # send data per line
    for l in f.readlines():
        data+=l
    f.close()
    data+="\r\n\r\n"


    # Split at line breaks
    requestMessage = request_string.splitlines()

    # Collecting the requestline (i.e. GET * HTTP/1.1)
    getRequestLine = requestMessage[0]

    # collecting the headers
    headers = requestMessage.pop(0)

    # Step 0: Split the string by line
    # parse the requestline and determine what data and code to give back
    parsedRequest = local_parser(getRequestLine, requestMessage)

    
    if "favicon" in request_string:
        data = "HTTP/1.1 404 Not Found\r\n\r\n"
        return data
    
    return parsedRequest


    # Fill in the code to handle the http request here. You will probably want
    # to write additional functions to parse the http request into a nicer data
    # structure (e.g., not a string) and to easily create http responses.

    # Used Figure 2.8 in book as guideline: Request line and Header lines
    
    
    
    raise NotImplementedError

    pass


# is given a get requestline and our headers
# then determines what codes and data to provide
def local_parser(getRequest, headers):
    data = ''

    ## Step 1: Get the first line (request line) and split into method, url, version
    ## Step 2: Until you see <CR><LF> (\r\n), read lines as key, value with header name and value. Store as a dictionary
    ## Step 3: Check to make sure method, url, and version are all compliant
    ## Step 3a: if method is a GET and url is "/" or "/index.html" and correct HTTP version, we need to respond with 200 OK and some HTML     
        ## Step 3b: If method is compliant, but not implemented, we need to respond with a correct HTTP response 
        ## Step 3c: If the version is not compliant, we need to respond with correct HTTP response
        ## Step 3d: If file does not exist in server path, respond with HTTP 404 File not found response
    ## Step 4: Checking to make sure headers are correctly formatted

    # split out get request into its three parts
    getCommands = getRequest.split()
    method = getCommands[0]
    url = getCommands[1]
    version = getCommands[2]

    
    # if requested url is in our server files
    status_code = '404'
    if (url == 'index.html' or url =='*') or (url == '/index.html' or url == '/'):
        status_code = '200' 

    else:
        data = "HTTP/1.1 404 Not Found\r\n\r\n"
        return data
        

    # if everything is fine, we return our success code and the percede the checks
    if (method == 'GET' and status_code == '200' and version == 'HTTP/1.1'):
        data = 'HTTP/1.1 200 OK\r\n'
        data+= 'Connection: keep-alive\r\n'
        data+= 'Content-Type: text/html; encoding=utf-8\r\n'
        f = open('index.html', 'r')
        # send data per line
        for l in f.readlines():
            data+=l
        f.close()
        data+="\r\n\r\n"

        ## webbrowser class to find path and open in a browser
        webbrowser.open('file://' + os.path.realpath('index.html'))


    # if our method is not implemented
    if (method != 'GET' and status_code == '200' and version == 'HTTP/1.1'):
        data = 'HTTP/1.1 501 Not Implemented\r\n'
        return data

    # if our version is not compliant
    if (method == 'GET' and status_code == '200' and version != 'HTTP/1.1'):
        data = 'HTTP/1.1 505 HTTP Version Not Supported\r\n'
        return data

    # if our file is nowhere to be found
    if (method == 'GET' and status_code == '404' and version != 'HTTP/1.1'):
        data = "HTTP/1.1 404 Not Found\r\n\r\n"
        return data


    # if our headers are formated properly
    newheaders = []

    # collects the headers and their details
    for i in headers:
        if i != '':
            newheaders += i.split(": ")
    

    heads  = []
    details = []

    # filters the head info for just the title
    index = 0
    while index <= (len(newheaders) - 1):
        if (index % 2 == 0):
            heads.append(newheaders[index])
        index += 1


    # filters the head info for just the details
    index = 0
    while index <= (len(newheaders) - 1):
        if (index % 2 == 1):
            details.append(newheaders[index])
        index += 1


    # creates a dictionary of headers and their details
    heads_dict = dict(zip(heads, details))

    # checks lengths of our headers and their data
    if (len(heads) != len(details)):
        data = "HTTP1.1 400 Bad Request\r\n\r\n"
        return data
    
    # checks if any header has no details and vice versa
    values = heads_dict.values()
    for d in values:
        if d == ' ' or d == '':    
            data = "HTTP1.1 400 Bad Request\r\n\r\n"
            index += 1

    
    return data
        

def clientThreads(connection, address):

    connected = True
    while connected:
        
        request=""
              
        received=connection.recv(1024).decode('utf-8')

        if received == "!DISCONNECT":
            connected = False
        
        request+=received

                
        reply = http_handle(request)
    
        # end thread here
                
        connection.sendall(reply.encode('utf-8'))

        print("\n\nReceived request")
        print("======================")
        print(request.rstrip())
        print("======================")



        print("\n\nReplied with")
        print("======================")
        print(reply.rstrip())
        print("======================")


    connection.close()  
    return 0




if __name__ == "__main__":
    sys.exit(main())
