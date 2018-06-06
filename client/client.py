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
    i = input("Enter a message to send (or :Q) to quit:")
    if i == ':Q':
        break
    else:
        client.send(i)

client.close()
