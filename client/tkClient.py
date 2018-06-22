import socket, json, asyncio, tkinter, sys

class messageList:
    def __init__(self, length):
        self.length = length
        self.items = [''] * length
        self.labels = [None] * length
    def addItem(self, text, color):
        self.items.pop(0)
        self.items.append(text)
        self.labels.pop(0)
        self.labels.append(tkinter.Label(root, text=text, font=("arial", 10, "bold"), fg=color))
    def print(self):
        for i in range(self.length):
            if not self.labels[i] == None:
                self.labels[i].place(x=10, y=i*20+10)


textList = messageList(12)

root = tkinter.Tk()
root.title("Chatroom")
root.geometry("400x300")
window = tkinter.PanedWindow(root)
message = tkinter.StringVar()
if sys.platform == 'darwin':
    #mac
    tkinter.Entry(root, textvariable=message, width=32, bg="white").place(x=10, y = 270)
    tkinter.Button(root, text="Send", width=5, height=1, bg="grey", command=lambda: send('m', message.get())).place(x=323, y=270)
else:
    #w-windows?
    tkinter.Entry(root, textvariable=message, width=50, bg="white").place(x=10, y = 270)
    tkinter.Button(root, text="Send", width=5, height=1, bg="grey", command=lambda: send('m', message.get())).place(x=335, y=266)

async def main():
    while True:
        root.update()
        await asyncio.sleep(0.01)

async def update():
    while True:
        received = receive()
        if not received == None:
            textList.addItem(received[1], received[0])
            textList.print()
        await asyncio.sleep(0.01)

def send(type, message):
    client.send(bytes(json.dumps((type, message)), 'utf-8'))

def receive():
    try:
        return json.loads(str(client.recv(512))[2:-1])
    except socket.timeout:
        return None

#creates client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(1)

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
name = input('Name: ')
send('n', name)



loop = asyncio.get_event_loop()
loop.create_task(main())
loop.create_task(update())
loop.run_forever()
loop.close()

root.mainloop()