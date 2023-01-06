# Web_Client_-_Server
Using TCP sockets we launch a local python server on port 1024, then a client socket can connect and communicate via HTTP                         
This server is also able to handle three telnet clients simultaneously, via threading

Usage:
python3 web_server.py (optional port specification with '--port' or '-p' + 'port number')

In a sperate terminal window, the client programs runs as;
python3 web_client.py

