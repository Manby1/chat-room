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

#individual socket handler
async def connection(client_socket, address):
    print('Now listening to connection:', address)
    while True:
        data = str(client_socket.recv(512))[2:-1]
        type = data[0]
        message = data[2:]
        if type == 'n':
            if address not in addresses:
                print(message+' has connected!')
            else:
                print(addresses[address]+' has changed their name to '+message+'!')
            addresses[address] = message
        elif type == 'm':
            print(addresses[address]+': '+message)
        #await asyncio.sleep(0.1)

#searches for new clients and allocates them their own loop
async def serverLoop(address, port, connections):
    #setup using ip and port
    server.bind((address, port))
    server.listen(connections)
    print('Server listening...')
    while True:
        (client_socket, address) = server.accept()
        print("Received an address!")
        task = loop.create_task(connection(client_socket, address))
        tasks.append(task)
        await asyncio.sleep(0.1)

tasks = [serverLoop(IP_address, Port, 5)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()