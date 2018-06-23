import socket, asyncio, json, random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
loop = asyncio.get_event_loop()

#automatic connection
with open('../server.txt') as f:
    data = f.read()
IP_address = data[0:13]
Port = int(data[14:17])
#address list - names
addresses = {}
#client objects
clients = {}

class client:
    def __init__(self, socket):
        self.socket = socket
        self.color = '#'+str(hex(random.randint(0, 256**3-1)))[2:]
    def setName(self, name):
        self.name = name
    def send(self, message):
        self.socket.send(bytes(json.dumps(message), 'utf-8'))
    def receive(self):
        try:
            return json.loads(str(self.socket.recv(512))[2:-1])
        except socket.timeout:
            return None

#manual connection
'''
IP_address = input('IP: ')
Port = int(input('Port: '))
'''

def sendToAll(color, message):
    for client in clients:
        client.send((color, message))

#individual socket handler
async def connection(client_socket, address):
    me = client(client_socket)
    clients[me] = me
    print('Now listening to connection:', address)
    clients[me].socket.settimeout(1)
    while True:
        try:
            data = clients[me].receive()
            #recieve and interpret data
            if not data == '' and not data == None:
                type = data[0]
                message = data[1]
                #rename command
                if type == 'n':
                    if address not in addresses:
                        output = message+' has connected!'
                        print(output)
                        sendToAll(clients[me].color, output)
                    else:
                        output = addresses[address]+' has changed their name to '+message+'!'
                        print(output)
                        sendToAll(clients[me].color, output)
                    addresses[address] = message

                #plain message
                elif type == 'm':
                    output = addresses[address]+': '+message
                    print(output)
                    sendToAll(clients[me].color, output)
        except ConnectionResetError:
            print(addresses)
            output = addresses[clients[me].socket.getpeername()]+' left...'
            print(output)
            clients[me].send(output)
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