import socket

#set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''
#input ip and port
IP_address = input("Enter IP Address to connect to:")
port = int(input("Enter Port to connect to:")'''

IP_address = input('IP: ')
port = int(input('Port: '))

#connect to ip and port
client.connect((IP_address, port))

while True:
    try:
        i = input("Enter a message to send or just hit enter to refresh.")
        if i != '':
            client.send(bytes(i,'utf-8'))
        (server_socket, address) = client.accept()
        print(address)
        while True:
            data = server_socket.recv(512)
            print("RECEIVED:",str(data)[2:-1])

    except Exception as e:
        print(e)
        client.close()
