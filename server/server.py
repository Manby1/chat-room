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

#adress list
addresses = {}

#setup using ip and port
server.bind((IP_address, port))
server.listen(5)

while True:
    try:
        (client_socket, address) = server.accept()
        if address in addresses:
            print(addresses[address])
        while True:
            data = str(client_socket.recv(512))[2:-1]
            if data[0] == '#':
                addresses[address]=data[1:]
            else:
                print("RECEIVED:",data)

    except Exception as e:
        print(e)
        server.close()