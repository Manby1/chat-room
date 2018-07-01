import socket, asyncio, json

class Client:
    def __init__(self, socket, address, clientid):
        self.socket = socket
        self.address = address
        self.name = None
        self.avatar = None
        self.ID = clientid
        self.buffer = []

    def send(self, message_type, message, raw=False):
        #RAW PARAMETER DOESN'T FILTER OUT SPLITTER CHARACTER
        #simplified send function
        #removes any of the delimiters from the message and puts it into a tuple with the type
        if raw:
            send_data = json.dumps((message_type, message))
        else:
            send_data = json.dumps((message_type, ''.join(message.split('\uFFFF'))))
        self.socket.send(bytes(send_data+'\uFFFF', 'utf-8'))

    def receive(self):
        try:
            m = self.socket.recv(2048)
            print(m)
            messages = m.decode().split('\uFFFF')
            if '' in messages:
                print("Found whole message sequence.")
                #WHOLE MESSAGE(S)
                if self.buffer == []:
                    print("Buffer empty: Treating as new.")
                    messages = [json.loads(i) for i in messages[:-1]]
                else:
                    print("Buffer full - appending to buffer {}.".format(self.buffer))
                    bufferend = ''.join(self.buffer)+messages[0]
                    messages = [json.loads(bufferend)]+[json.loads(i) for i in messages[1:-1]]
                    self.buffer = []
            else:
                #CONTAINS PACKET
                if len(messages) == 1:
                    #ONLY A SINGLE PACKET
                    print("Found single packet.")
                    if self.buffer == []:
                        print("Buffer empty. Appending...")
                        self.buffer.append(messages[0])
                        messages = None
                    else:
                        print("Buffer full. No splitter received - appending...")
                        self.buffer.append(messages[0])
                        messages = None
                else:
                    #WHOLE MESSAGES = LENGTH-1 + SINGLE PACKET AT END
                    print("Found buried packet.")
                    if self.buffer == []:
                        print("Buffer empty.")
                        self.buffer.append(messages[-1])
                        messages = [json.loads(i) for i in messages[:-1]]
                    else:
                        print("Buffer full.")
                        bufferend = ''.join(self.buffer) + messages[0]
                        self.buffer = [messages[-1]]
                        messages = [json.loads(bufferend)]+[json.loads(i) for i in messages[1:-1]]

            print("Done!")
            return messages

            '''OLD WAY OF DOING IT
            if len(messages) > 1 and messages[-1] == '':
                #WHOLE MESSAGE - MESSAGE + SPLITTER
                if self.buffer == []:
                    messages = [json.loads(i.replace("'",'"')) for i in messages[:-1]]
                else:
                    print(''.join(self.buffer)+''.join(messages[:-1])+'\n')
                    messages = [json.loads(i.replace("'",'"')) for i in ''.join(self.buffer)+''.join(messages[:-1])]
                    self.buffer = []
            elif len(messages) > 1 and messages[-1] != '':
                #WHOLE MESSAGE + PACKET
                #The packet should be the first in its sequence, as it was sent after a whole message
                if self.buffer == []:
                    messages = [json.loads(i.replace("'",'"')) for i in messages[:-1]]
                else:

            elif len(messages) == 1:
                #SINGLE PACKET
                self.buffer.append(messages[0])
                print(''.join(self.buffer)+'\n')
            else:
                print("ERROR: Received strange length message:",messages)
            return messages
        '''
        except socket.timeout:
            return None


class Server(socket.socket):
    def __init__(self, IP_address, Port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_address = IP_address
        self.Port = Port
        self.clients = []
        self.clientidinc = 0
    
    def sendToAll(self, message_type, message, raw=False):
        for clientobj in self.clients:
            clientobj.send(message_type, message, raw=raw)

    async def clientLoop(self, client_socket, address):
        current_client = Client(client_socket, address, self.clientidinc)
        self.clientidinc += 1
        self.clients.append(current_client)
        print("I can hear the messages of {} from far away...".format(address))
        current_client.socket.settimeout(0.5)
        while current_client in self.clients:
            try:
                data = current_client.receive()
                if data:
                    for raw_message in data:
                        print("RAW: {}\n".format(raw_message))
                        message_type = raw_message[0]
                        message = raw_message[1]
                        print(message_type)
                        if message_type == 'N':
                            if current_client.name == None:
                                output = "{} has connected!".format(message)
                                current_client.name = message
                                print(output)
                                self.sendToAll('S',output)
                            else:
                                output = "{} has changed their name to {}!".format(current_client.name, message)
                                print(output)
                                self.sendToAll('S',output)

                        elif message_type == 'M':
                            output = "{}: {}".format(current_client.name, message)
                            print(output)
                            self.sendToAll('S', output)

                        elif message_type == 'I':
                            print("Received I type.")
                            current_client.avatar = message
                            print("Received an avatar from {}. Looks kinda sketch.".format(current_client.name))
                            self.sendToAll('I',message,raw=True)

            except ConnectionResetError:
                print("Wah!! {} left! Did I do something wrong? (｡•́︿•̀｡)".format(current_client.name))
                self.clients.remove(current_client)
                output = '{} has left...'.format(current_client.name)
                self.sendToAll('S',output)
                
            await asyncio.sleep(0.1)

    async def serverLoop(self, max_users):
        self.bind((self.IP_address, self.Port))
        self.listen(max_users)
        self.settimeout(1)
        print("I have been awakened. I can hear the sounds of the wind...")

        while True:
            try:
                client_socket, address = self.accept()
                print('W-we have a new client!! I really look forward to working with them...')
                asyncio.ensure_future(self.clientLoop(client_socket, address))

            except socket.timeout:
                pass

            await asyncio.sleep(0.1)


if __name__ == '__main__':
    #automatic connection via file with details
    try:
        with open('server.txt') as f:
            data = f.read().split('\n')
        IP_address, Port = data[0],data[1]
        Port = int(Port)
    except:
        print('Error reading server file. Please input manually.')
        IP_address = input('IP Address: ')
        Port = int(input('Port: '))
    
    server = Server(IP_address, Port)
    #event loop for multitasking
    loop = asyncio.get_event_loop()

    loop.create_task(server.serverLoop(5))
    loop.run_forever()
    loop.close()
