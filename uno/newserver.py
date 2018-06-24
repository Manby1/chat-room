import socket, asyncio, json, random

#Issues:
#No end character
#Port as letters will crash the script

class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.name = None

    def send(self, message_type, message):
        #simplified send function
        #removes any of the delimiters from the message and puts it into a tuple with the type
        send_data = (message_type, ''.join(message.split('\uFFFF')))
        self.socket.send(bytes(json.dumps(send_data)+'\uFFFF', 'utf-8'))

    def receive(self):
        try:
            messages = self.socket.recv(512).decode().split('\uFFFF')
            messages = [json.dumps(i) for i in messages[:-1]]
        except socket.timeout:
            return None


class Server:
    def __init__(self, IP_address, Port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_address = IP_address
        self.Port = Port
        self.clients = []
    
    def sendToAll(self, message_type, message):
        for clientobj in self.clients:
            clientobj.send(message_type, message)

    async def clientLoop(self, client_socket, address):
        current_client = Client(client_socket, address)
        self.clients.append(current_client)
        print("I can hear the messages of {} from far away...".format(address))
        current_client.socket.setttimeout(0.5)
        while current_client in clients:
            try:
                data = current_client.receive()
                if data:
                    for raw_message in data:
                        message_type = raw_message[0]
                        message = raw_message[1]

                        if message_type == 'N':
                            if current_client.name = None:
                                output = "{} has connected!".format(message)
                                print(output)
                                self.sendToAll('S',output)
                            else:
                                output = "{} has changed their name to {}!".format(current.client.name, message)
                                print(output)
                                self.sendToAll('S',output)

                        elif message_type == 'M':
                            output = "{}: {}".format(current_client.name, message)
                            print(output)
                            self.sendToAll('S', output)

            except ConnectionResetError:
                print("Wah!! {} left! Did I do something wrong? (｡•́︿•̀｡)".format(current_client.name))
                self.clients.remove(current_client)
                self.sendToAll('{} has left...'.format(current_client.name))

    async def serverLoop(self, max_users):
        self.socket.bind((self.IP_address, self.Port))
        server.listen(max_users)
        server.settimeout(1)
        print("I have been awakened. I can hear the sounds of the wind...")

        while True:
            try:
                client_socket, address = server.accept()
                print('W-we have a new client!! I really look forward to working with them...')
                asyncio.ensure_future(clientLoop(client_socket, address))

            except socket.timeout:
                pass

            await asyncio.sleep(0.1)


if __name__ == '__main__':
    #serversocket and asyncio event loop for multitasking
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    loop = asyncio.get_event_loop()

    #automatic connection via file with details
    try:
        with open('server.txt') as f:
            data = f.read()
        IP_address, Port = data.split('\n')
        Port = int(Port)
    except:
        print('Error reading server file. Please input manually.')
        IP_address = input('IP Address: ')
        Port = int(input('Port: '))
