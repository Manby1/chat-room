import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#input ip and port
IP_address = input("Enter IP Address to connect to:")
port = int(input("Enter Port to connect to:"))

#connect to ip and port
server.bind((IP_address, port))

#main loop -NOTE no asynchronous capabilities -only one connection will work
while True:
    pass
    #honestly im dealing with the realisation that we might have to just use async here...