import socket, asyncio, json, random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
loop = asyncio.get_event_loop()

#automatic connection
with open('../server.txt') as f:
    data = f.read()
IP_address = data[0:13]
Port = int(data[14:17])
#client objects
clients = {}

class client:
    def __init__(self, socket):
        self.socket = socket
        self.color = '#'+str(hex(random.randint(0, 256**3-1)))[2:]
        self.name = None
    def setName(self, name):
        self.name = name
    def send(self, message):
        self.socket.send(bytes(json.dumps(message), 'utf-8'))
    def receive(self):
        try:
            msgs = split(self.socket.recv(512).decode())
            return list(map(lambda msg: json.loads(msg), msgs))
        except socket.timeout:
            return []

def split(text):
    items = []
    string = ''
    for i in text:
        string += i
        if i == ']':
            items.append(string)
            string = ''
    return items

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
    clients[me].socket.settimeout(0.5)
    while me in clients:
        try:
            data = clients[me].receive()
            #recieve and interpret data
            if not data == []:
                for msg in data:
                    type = msg[0]
                    message = msg[1]
                    #rename command
                    if type == 'n':
                        if clients[me].name == None:
                            output = message+' has connected!'
                            print(output)
                            sendToAll(clients[me].color, output)
                        else:
                            output = clients[me].name+' has changed their name to '+message+'!'
                            print(output)
                            sendToAll(clients[me].color, output)
                        clients[me].name = message

                    #plain message
                    elif type == 'm':
                        output = clients[me].name+': '+message
                        print(output)
                        sendToAll(clients[me].color, output)
        except ConnectionResetError:
            output = clients[me].name+' left...'
            print(output)
            color = clients[me].color
            clients.pop(clients[me])
            sendToAll(color, output)
        await asyncio.sleep(0.1)
    print('Client loop ended.')

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