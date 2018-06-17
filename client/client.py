import socket

#creates client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#automatic connection
with open('../server.txt') as f:
    data = f.read()
IP_address = data[0:13]
Port = int(data[14:17])

#manual connection
'''
IP_address = input('IP: ')
Port = int(input('Port: '))
'''

#message encoder
commands = {'message':'m|', 'name':'n|'}
def send(message, type):
    client.send(bytes(commands[type]+str(message), 'utf-8'))

#nickname
name = input('Name?\n')

#connect to ip and port
try:
    client.connect((IP_address, Port))
except ConnectionRefusedError:
    print('No server found.')

print('Connected!')

#sends name
send(name, 'name')

while True:
    try:
        i = input("Enter a message to send.\n")
        if i[0:2] == 'n|':
            send(i[2:], 'name')
        else:
            send(i, 'message')

    except Exception as e:
        print(e)
        client.close()
