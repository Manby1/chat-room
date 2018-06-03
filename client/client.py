import socket

#set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#input ip and port
IP_address = input("Enter IP Address to connect to:")
port = int(input("Enter Port to connect to:"))

#connect to ip and port
client.connect((IP_address, port))

