import socket, asyncio, json

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

#individual socket handler
async def connection(client_socket, address):
    print('Now listening to connection:', address)
    client_socket.settimeout(1)
    while True:
        try:
            #recieve and interpret data
            data = str(client_socket.recv(512))[2:-1]
            type = data[0]
            message = data[2:]

            #rename command
            if type == 'n':
                if address not in addresses:
                    output = message+' has connected!'
                    print(output)
                else:
                    output = addresses[address]+' has changed their name to '+message+'!'
                    print(output)
                addresses[address] = message

            #plain message
            elif type == 'm':
                output = addresses[address]+': '+message
                print(output)
                client_socket.send(bytes(output, 'utf-8'))

        except socket.timeout:
            pass
        await asyncio.sleep(0.1)

#searches for new clients and allocates them their own loop
async def serverLoop(address, port, connections):
    # setup using ip and port
    server.bind((address, port))
    server.listen(connections)
    server.settimeout(1)
    print('Server listening...')

    while True:
        try:
            (client_socket, address) = server.accept()
            print("Received an address!")
            asyncio.ensure_future(connection(client_socket, address))
        except socket.timeout:
            pass
        await asyncio.sleep(0.1)

loop.create_task(serverLoop(IP_address, Port, 5))
loop.run_forever()
loop.close()