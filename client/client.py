import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

f = open('server.txt')
file = f.read()
IP_address = file[0:13]
port = int(file[14:17])

'''
IP_address = input('IP: ')
port = int(input('Port: '))
'''

#connect to ip and port
client.connect((IP_address, port))

name = input('Name?\n')
client.send(bytes(name, 'utf-8'))

while True:
    try:
        i = input("Enter a message to send.\n")
        client.send(bytes(i, 'utf-8'))

    except Exception as e:
        print(e)
        client.close()
