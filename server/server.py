import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

f = open('server.txt')
file = f.read()
IP_address = file[0:13]
port = int(file[14:17])

'''
IP_address = input('IP: ')
port = int(input('Port: '))
'''

#setup using ip and port
server.bind((IP_address, port))
server.listen(5)

while True:
    try:
        (client_socket, address) = server.accept()
        print(address)
        while True:
            data = client_socket.recv(512)
            print("RECEIVED:",str(data)[2:-1])

    except Exception as e:
        print(e)
        server.close()