import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open('server.txt') as f:
    data = f.read()
IP_address = data[0:13]
Port = int(data[14:17])

'''
IP_address = input('IP: ')
port = int(input('Port: '))
'''

#address list
addresses = {}

#setup using ip and port
server.bind((IP_address, port))
server.listen(5)

while True:
    try:
        (client_socket, address) = server.accept()
        print('New connection:', address)
        while True:
            data = str(client_socket.recv(512))[2:-1]
            if not address in addresses:
                addresses[address] = data
            else:
                print(addresses[address], data)

    except Exception as e:
        print(e)
        server.close()