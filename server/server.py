import socket, asyncio

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
loop = asyncio.get_event_loop()

#automatic connection
with open('../server.txt') as f:
    data = f.read()
IP_address = data[0:13]
Port = int(data[14:17])
#address list - names
addresses = {}

#manual connection
'''
IP_address = input('IP: ')
Port = int(input('Port: '))
'''

def recieve():
    data = str(client_socket.recv(512))[2:-1]
    type = data[:1]
    message = data[2:]
    return type, message


async def connection(client_socket, address):
    print('Now listening to connection:', address)
    while True:
        type, message = recieve()
        if type == 'n':
            addresses[address] = message
        elif type == 'm':
            print(addresses[address], message)

async def serverLoop(address, port, connections):
    #setup using ip and port
    server.bind((address, port))
    server.listen(connections)
    print('Server listening...')
    while True:
        try:
            (client_socket, address) = server.accept()
            await connection(client_socket, address)

        except Exception as e:
            print(e)
            server.close()

loop.run_until_complete(serverLoop(IP_address, Port, 5))
loop.close()