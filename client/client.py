import socket

#set up client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = input('IP: ')
port = int(input('Port: '))

#connect to ip and port
client.connect((IP_address, port))

while True:
    try:
        i = input("Enter a message to send.\n")
        client.send(bytes(i,'utf-8'))

    except Exception as e:
        print(e)
        client.close()
