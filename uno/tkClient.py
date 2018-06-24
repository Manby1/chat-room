import socket, json, asyncio, sys, pygame

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

#This comment is here because git was trying to make me merge and commit my 0 Changes.

def boxSend():
    if not message.get() == '':
        send('m', message.get())
        box.delete(0, 'end')

textList = messageList(12)

root = tkinter.Tk()
root.title("Chatroom")
root.geometry("400x300")
window = tkinter.PanedWindow(root)
message = tkinter.StringVar()
if sys.platform == 'darwin':
    #mac
    box = tkinter.Entry(root, textvariable=message, width=32, bg="white")
    box.place(x=10, y = 270)
    box.bind('<Return>', lambda event: boxSend())
    tkinter.Button(root, text="Send", width=5, height=1, bg="grey", command=boxSend).place(x=323, y=270)
else:
    #w-windows?
    box = tkinter.Entry(root, textvariable=message, width=50, bg="white")
    box.place(x=10, y = 270)
    box.bind('<Return>', lambda event: boxSend())
    tkinter.Button(root, text="Send", width=5, height=1, bg="grey", command=boxSend).place(x=335, y=266)

async def main():
    running = True
    while running:
        try:
            root.update()
            await asyncio.sleep(0.01)
        except tkinter.TclError:
            running = False
    client.close()
    loop.close()
    quit()

async def update():
    while True:
        received = receive()
        if not received == []:
            for msg in received:
                textList.addItem(msg[1], msg[0])
            textList.print()
        await asyncio.sleep(0.01)

def send(type, message):
    print(type, message)
    client.send(bytes(json.dumps((type, message)), 'utf-8'))

def receive():
    try:
        msgs = split(client.recv(512).decode())
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

#creates client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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

client.settimeout(0.1)

#sends nickname
name = input('Name: ')
send('n', name)



loop = asyncio.get_event_loop()
loop.create_task(main())
loop.create_task(update())
loop.run_forever()
loop.close()

root.mainloop()