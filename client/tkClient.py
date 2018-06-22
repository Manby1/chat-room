import socket, json, asyncio, tkinter

#creates client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class logc:
    def __init__(self):
        self.log = []

log = logc()

#message encoder
def send(message, type):
    client.send(bytes(commands[type] + str(message), 'utf-8'))

commands = {'message':'m|', 'name':'n|', 'receive':'r|'}

def handleSend(message):
    message = message.get()
    try:
        # if input is a command
        if message[0] == '/':
            # rename command
            if message[1:6] == 'name ':
                send(message[6:], 'name')
                print('Changed name to ' + message[6:] + '!')

        # otherwise, send it as a plain message
        else:
            send(message, 'message')

    # server closed
    except ConnectionResetError:
        print('Server was closed.')
        client.close()

root = tkinter.Tk()
root.title("Enter GameID")
root.geometry("400x300")
window = tkinter.PanedWindow(root)
heading = tkinter.Label(root, text="Message:", font=("arial", 10, "bold"), fg="violet").place(x=10, y=10)
message = tkinter.StringVar()
idbox = tkinter.Entry(root, textvariable=message, width=25, bg="white").place(x=10, y = 30)
sendButton = tkinter.Button(root, text="Send", width=25, height=5, bg="grey", command=lambda: handleSend(message)).place(x=10, y=50)



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
            data = str(client.recv(512))[2:-1]
            log.log.append(data)
        except socket.timeout:
            pass
        except ConnectionResetError:
            print('Server was closed.')
            client.close()
            quit()
        await asyncio.sleep(0.1)

'''async def sendLoop():
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

        await asyncio.sleep(0.1)'''

loop = asyncio.get_event_loop()
loop.create_task(root.mainloop())
loop.create_task(receiveLoop())
loop.run_forever()
loop.close()

root.mainloop()