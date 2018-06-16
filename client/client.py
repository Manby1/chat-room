import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with open('../server.txt') as f:
    data = f.read()
IP_address = data[0:13]
Port = int(data[14:17])

commands = {'message':'m|', 'command':'c|'}
def send(message, type):
    client.send(bytes(commands[type]+str(message), 'utf-8'))

#connect to ip and port
client.connect((IP_address, Port))

name = input('Name?\n')
send(name, 'command')

while True:
    try:
        i = input("Enter a message to send.\n")
        send(i, 'message')

    except Exception as e:
        print(e)
        client.close()
