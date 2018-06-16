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

async def connection(client_socket, address):
    print('Now listening to connection:', address)
    while True:
        data = str(client_socket.recv(512))[2:-1]
        if not address in addresses:
            addresses[address] = data
        print(addresses[address], data)

async def serverLoop(address, port, connections):
    #setup using ip and port
    server.bind((address, port))
    server.listen(connections)
    print('Server listening...')
    while True:
        try:
            (client_socket, address) = server.accept()
            loop.create_task(connection(client_socket, address))

        except Exception as e:
            print(e)
            server.close()

loop.create_task(serverLoop(IP_address, Port, 5))
loop.run_forever()
loop.close()