import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = 192.168.1.117
port = 843

#setup using ip and port
server.bind((IP_address, port))