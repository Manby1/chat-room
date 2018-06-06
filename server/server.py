import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = input('IP: ')
port = int(input('Port: '))

#setup using ip and port
server.bind((IP_address, port))
server.listen(1)

while True:
    (clientsocket, address) = server.accept()
    print(clientsocket, address)

server.close()