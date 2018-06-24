import socket, json, asyncio

#creates client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class logc:
    def __init__(self):
        self.log = []

log = logc()

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
commands = {'message':'m|', 'name':'n|', 'receive':'r|'}
def send(message, type):
    client.send(bytes(commands[type]+str(message), 'utf-8'))

#nickname
name = input('Name?\n')

#connect to ip and port
trying = True
while trying:
    print('Searching for server...')
    try:
        client.connect((IP_address, Port))
        print('Connected!')
        trying = False
    except ConnectionRefusedError:
        print('No server found.')
        if not input('Try again? (Y/N)\n').upper() == 'Y':
            trying = False
            quit()

#sends nickname
send(name, 'name')

client.settimeout(1)


async def receiveLoop():
    while True:
        try:
            data = client.recv(512).decode()
            log.log.append(data)
        except socket.timeout:
            pass
        except ConnectionResetError:
            print('Server was closed.')
            client.close()
            quit()
        await asyncio.sleep(0.1)

async def sendLoop():
    while True:
        try:
            i = input("Enter a message to send.\n")

            #recieve messages
            if i == '':
                print('###LOG###')
                if not log.log == []:
                    for i in log.log:
                        print(i)
                    log.log = []
                else:
                    print('No new messages.')
                print('#########\n')

            #if input is a command
            elif i[0] == '/':
                #rename command
                if i[1:6] == 'name ':
                    send(i[6:], 'name')
                    print('Changed name to '+i[6:]+'!')

            #otherwise, send it as a plain message
            else:
                send(i, 'message')

        #server closed
        except ConnectionResetError:
            print('Server was closed.')
            client.close()
            break

        await asyncio.sleep(0.1)

loop = asyncio.get_event_loop()
loop.create_task(receiveLoop())
loop.create_task(sendLoop())
loop.run_forever()
loop.close()