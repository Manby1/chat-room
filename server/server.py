import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(server.get)
#IP_address = input('IP: ')
port = int(input('Port: '))

#setup using ip and port
serversocket.bind((server.gethostname(), port))
server.listen(2)

while True:
    try:
        (clientsocket, address) = server.accept()
        print(clientsocket, address)

    except Exception as e:
        print(e)
        server.close()