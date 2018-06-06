import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = input('IP: ')
port = int(input('Port: '))

#setup using ip and port
server.bind((socket.gethostname(), port))
server.listen(2)

while True:
    try:
        (client_socket, address) = server.accept()
        print(address)
        while True:
            data = client_socket.recv(512)
            print("RECIEVED:",data)

    except Exception as e:
        print(e)
        server.close()