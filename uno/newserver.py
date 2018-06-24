import socket, asyncio, json, random

#Issues:
#No end character
#Port as letters will crash the script

class Client:
    def __init__(self, socket):
        self.socket = socket

    def send(self, message):
        #simplified send function
        self.socket.send(bytes(json.dumps(message), 'utf-8'))
    def receive(self):
        try:
            messages = self.socket.recv(512).decode()
        except socket.timeout:
            return None

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

    #client objects
    clients = {}
