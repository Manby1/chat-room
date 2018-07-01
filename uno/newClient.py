import pygame, asyncio, socket, sys, json

pygame.init()
pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.display.set_caption('Uno!')

displayInfo = pygame.display.Info()
res = (displayInfo.current_w, displayInfo.current_h)
if res == (1280,800) and sys.platform == 'darwin':
    display = pygame.display.set_mode((1000, 709))
else:
    display = pygame.display.set_mode((1000, 800))

#Mouse Object
class Mouse:
    def __init__(self):
        self.pressed = pygame.mouse.get_pressed()
        self.update()
        self.is_dragging = None
        self.buttons = {'left':0, 'right':2, 'middle':1}

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.prev_pressed = self.pressed
        self.pressed = pygame.mouse.get_pressed()

    def press(self, button='left'):
        button = self.buttons[button]
        if self.pressed[button]:
            return True
        return False

    def click(self, obj, button='left'):
        button = self.buttons[button]
        if self.hover(obj):
            if not self.prev_pressed[button] and self.pressed[button]:
                return True
        return False

    #Couldn't this be an option for click instead?
    def clickScreen(self, button='left'):
        button = self.buttons[button]
        if not self.prev_pressed[button] and self.pressed[button]:
            return True
        return False

    def hover(self, obj):
        if self.pos[0] in range(obj.rect[0], obj.rect[0] + obj.rect[2]) and self.pos[1] in range(obj.rect[1], obj.rect[1] + obj.rect[3]):
            return True
        return False

    def holding(self, obj, button):
        button = self.buttons[button]
        if self.hover(obj) and self.pressed[button]:
                return True
        return False

    def dragging(self, obj):
        if self.click(obj, 'left') and self.holding(obj, 'left') and self.is_dragging == None:
            self.is_dragging = obj
            self.drag_offset = (obj.center[0] - self.pos[0], obj.center[1] - self.pos[1])
            return True
        elif self.is_dragging == obj and self.pressed[0]:
            return True
        if self.is_dragging == obj:
            self.is_dragging = None
        return False

#GUI Text
class Text:
    def __init__(self, pos, text, font_size, font_colour = (0, 0, 0)):
        self.formatted_font = pygame.font.Font('Login.ttf', font_size)
        self.text = self.formatted_font.render(text, True, font_colour)
        self.font_size = font_size

        self.position(pos)
    def position(self, pos):
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.center = pos

    def print(self):
        display.blit(self.text, self.text_rect)

#GUI Buttons
class Button:
    def __init__(self, pos, text, font_size, border_size = 0, border_colour = (0, 0, 0), colour = (255, 200, 100), font_colour = (0, 0, 0), width = None, height = None):
        self.colour = colour
        self.border_size = border_size
        self.border_colour = border_colour
        self.formatted_font = pygame.font.Font('Login.ttf', font_size)
        self.text = self.formatted_font.render(text, True, font_colour)
        self.font_size = font_size
        self.width = width
        self.height = height

        self.position(pos)
    def position(self, pos):
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.center = pos
        if self.width == None:
            self.width = self.text_rect[2] + self.font_size * 2
        if self.height == None:
            self.height = self.text_rect[3] + self.font_size * 2
        self.rect = (round(self.center[0] - self.width / 2), round(self.center[1] - self.height / 2), self.width, self.height)

    def print(self):
        if not self.border_size == 0:
            pygame.draw.rect(display, self.border_colour, self.rect)
            pygame.draw.rect(display, self.colour, (self.rect[0]+self.border_size, self.rect[1]+self.border_size, self.rect[2]-self.border_size*2, self.rect[3]-self.border_size*2))
        else:
            pygame.draw.rect(display, self.colour, self.rect)
        display.blit(self.text, self.text_rect)

#GUI Box
class Box:
    def __init__(self, pos, width, height, border_size = 0, border_colour = (0, 0, 0), colour = (255, 200, 100)):
        self.colour = colour
        self.border_size = border_size
        self.border_colour = border_colour
        self.width = width
        self.height = height

        self.position(pos)
    def position(self, pos):
        self.center = pos
        self.rect = (round(self.center[0] - self.width / 2), round(self.center[1] - self.height / 2), self.width, self.height)

    def print(self):
        if not self.border_size == 0:
            pygame.draw.rect(display, self.border_colour, self.rect)
            pygame.draw.rect(display, self.colour, (self.rect[0]+self.border_size, self.rect[1]+self.border_size, self.rect[2]-self.border_size*2, self.rect[3]-self.border_size*2))
        else:
            pygame.draw.rect(display, self.colour, self.rect)

#GUI Entry Boxes
class Entry:
    def __init__(self, pos, font_size, border_size = 0, border_colour = (0, 0, 0), colour = (255, 200, 100), font_colour = (0, 0, 0), width = None, height = None, highlight_colour = (255, 255, 0)):
        self.colour = colour
        self.highlighted = False
        self.highlight_colour = highlight_colour
        self.border_size = border_size
        self.border_colour = border_colour
        self.font_colour = font_colour
        self.formatted_font = pygame.font.Font('Login.ttf', font_size)
        self.raw_text = ''
        self.text = self.formatted_font.render('', True, font_colour)
        self.font_size = font_size
        self.width = width
        self.height = height

        self.position(pos)
    def position(self, pos):
        self.center = pos
        self.text_rect = self.text.get_rect()
        if self.height == None:
            self.height = self.text_rect[3] + self.font_size * 0.8
        self.rect = (round(self.center[0] - self.width / 2), round(self.center[1] - self.height / 2), round(self.width), round(self.height))
        self.text_rect.center = (self.text_rect.center[0], pos[1])
        self.text_rect = self.text_rect.move(self.rect[0]+self.border_size+self.width/100, 0)

    def highlight(self, state):
        self.highlighted = state
        self.print()

    def newCharacter(self, char):
        if not char == None:
            self.raw_text += char
        else:
            self.raw_text = self.raw_text[:-1]
        self.text = self.formatted_font.render(self.raw_text, True, self.font_colour)
        display.blit(self.text, self.text_rect)
        self.print()

    def print(self):
        if not self.border_size == 0:
            if self.highlighted:
                colour = self.highlight_colour
            else:
                colour = self.border_colour
            pygame.draw.rect(display, colour, self.rect)
            pygame.draw.rect(display, self.colour, (self.rect[0]+self.border_size, self.rect[1]+self.border_size, self.rect[2]-self.border_size*2, self.rect[3]-self.border_size*2))
        else:
            pygame.draw.rect(display, self.colour, self.rect)
        display.blit(self.text, self.text_rect)

#Player Info Box
class PlayerInfo:
    def __init__(self, pos, border_colour = (0, 0, 0), colour = (255, 200, 100), font_colour = (0, 0, 0)):
        self.colour = colour
        self.border_size = 10
        self.border_colour = border_colour
        self.font_colour = font_colour
        self.formatted_font = pygame.font.Font('Login.ttf', 30)
        self.raw_text = 'Player'
        self.text = self.formatted_font.render(self.raw_text, True, font_colour)
        self.font_size = 30
        self.width = 650
        self.height = 60

        self.position(pos)
    def position(self, pos):
        self.center = pos
        self.text_rect = self.text.get_rect()
        self.rect = (round(self.center[0] - self.width / 2), round(self.center[1] - self.height / 2), round(self.width), round(self.height))
        self.text_rect.center = (self.text_rect.center[0], pos[1])
        self.text_rect = self.text_rect.move(self.rect[0]+self.border_size+self.width/100, 0)

    def setText(self, text):
        self.raw_text = text
        self.text = self.formatted_font.render(self.raw_text, True, self.font_colour)
        self.print()

    def setColour(self, font_colour, colour, border_colour):
        self.font_colour = font_colour
        self.text = self.formatted_font.render(self.raw_text, True, font_colour)
        self.colour = colour
        self.border_colour = border_colour
        self.print()

    def print(self):
        pygame.draw.rect(display, self.border_colour, self.rect)
        pygame.draw.rect(display, self.colour, (self.rect[0]+self.border_size, self.rect[1]+self.border_size, self.rect[2]-self.border_size*2, self.rect[3]-self.border_size*2))
        display.blit(self.text, self.text_rect)


#Screen
class Screen:
    def __init__(self):
        self.currentScreen = None
        self.active_widgets = None
        self.using = None
        self.phase = 0
        self.width, self.height = display.get_size()

        #title widgets
        title_play = Button((300, 600), 'Play!', 50, 20, (60, 60, 255), colour=(80, 80, 255), font_colour=(220, 220, 255), width = 240, height = 150)
        title_quit = Button((700, 600), 'Quit', 50, 20, (200, 0, 0), colour=(255, 0, 50), font_colour=(255, 220, 220), width = 240, height = 150)
        title_splash = Image('splash.png', (500, 250))

        #play widgets
        play_title = Text((500, 70), 'Play Uno!', 80, font_colour=(70, 200, 200))
        play_host = Button((300, 400), 'Host', 55, colour=(140, 25, 240), font_colour=(255, 255, 255), border_size=30, border_colour=(110, 5, 200), width = 240, height = 150)
        play_join = Button((700, 400), 'Join', 55, colour=(255, 255, 0), font_colour=(0, 0, 0), border_size=30, border_colour = (200, 200, 0), width = 240, height = 150)

        #join widgets
        join_title = Text((500, 70), 'Join Game', 80, font_colour=(160, 160, 50))
        join_ip = Entry((500, 300), 40, 5, (0, 0, 0), (255, 255, 255), (0, 0, 0), 600, highlight_colour=(70, 255, 255))
        join_port = Entry((500, 430), 40, 5, (0, 0, 0), (255, 255, 255), (0, 0, 0), 600, highlight_colour=(70, 255, 255))
        join_join = Button((700, 580), 'Join', 35, colour=(0, 255, 0), font_colour=(0, 0, 0), border_size=10, border_colour=(0, 200, 0))
        join_auto = Button((300, 580), 'Auto-Connect', 35, colour=(255, 255, 255), font_colour=(0, 0, 0), border_size=10, border_colour=(0, 0, 0))
        join_ip_text = Text((500, 250), 'IP Address:', 30)
        join_port_text = Text((500, 380), 'Port:', 30)
        join_fail = Box((500, 400), 500, 200, 10, (200, 0, 0), (255, 0, 50))
        join_failmsg = Text((500, 360), "Could not Connect", 40)
        join_ok = Button((500, 440), 'Ok', 30, colour=(180, 180, 180), font_colour=(50, 50, 50), border_size=5, border_colour=(100, 100, 100), width=150, height=80)

        #name widgets
        name_title = Text((500, 70), 'Connected!', 80, font_colour=(160, 160, 50))
        name_name = Entry((500, 400), 40, 5, (0, 0, 0), (255, 255, 255), (0, 0, 0), 600, highlight_colour=(70, 255, 255))
        name_name_text = Text((500, 350), 'Name:', 30)
        name_go = Button((500, 580), 'GO!', 35, colour=(0, 255, 0), font_colour=(0, 0, 0), border_size=10, border_colour=(0, 200, 0))

        #lobby widgets
        lobby_title = Text((500, 70), 'In Lobby', 80, font_colour=(200, 60 ,60))
        lobby_leave = Button((55, 30), 'Leave', 20, colour=(255, 0, 50), font_colour=(255, 220, 220), border_size=5, border_colour=(200, 0, 0), width=90, height=40)
        lobby_player1 = PlayerInfo((340, 320), (0, 0, 0), (0, 255, 0))
        lobby_confirm = Box((500, 400), 400, 200, 10, (200, 0, 0), (255, 0, 50))
        lobby_usure = Text((500, 360), 'Are you sure?', 40)
        lobby_yes = Button((400, 440), 'Yes', 30, colour=(255, 255, 255), font_colour=(0, 255, 0), border_size=5, border_colour=(0, 0, 0), width=150, height=80)
        lobby_no = Button((600, 440), 'No', 30, colour=(255, 255, 255), font_colour=(255, 0, 0), border_size=5, border_colour=(0, 0, 0), width=150, height=80)

        #universal
        back = Button((50, 30), 'Back', 20, colour=(50, 50, 50), font_colour=(255, 255, 255), border_size=5, border_colour=(0, 0, 0), width=80, height=40)

        #list of screens and their widgets
        self.screens = {
                        'title':{'play':(title_play, 0), 'quit':(title_quit, 0), 'splash':(title_splash, 0)},

                        'play':{'title':(play_title, 0), 'host':(play_host, 0), 'join':(play_join, 0), 'back':(back, 0)},

                        'join':{'title':(join_title, 0), 'ip_text':(join_ip_text, 0), 'port_text':(join_port_text, 0),
                                'ip':(join_ip, 0), 'port':(join_port, 0), 'join':(join_join, 0), 'back':(back, 0),
                                'auto':(join_auto, 0), 'fail':(join_fail, 1), 'failmsg':(join_failmsg, 1),
                                'ok':(join_ok, 1)},

                        'name':{'title':(name_title, 0), 'name_text':(name_name_text, 0), 'name':(name_name, 0),
                                'go':(name_go, 0), 'back':(back, 0)},

                        'lobby':{'leave':(lobby_leave , 0), 'title':(lobby_title, 0), 'player1':(lobby_player1, 0),
                                 'confirm':(lobby_confirm, 1), 'usure':(lobby_usure, 1), 'yes':(lobby_yes, 1),
                                 'no':(lobby_no, 1)}
                        }


    def switchScreen(self, screen):
        self.phase = 0
        self.active_widgets = self.screens[screen]
        self.current_screen = screen

    def dim(self):
        rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        rect.fill((0, 0, 0, 120))
        display.blit(rect, (0, 0))

    def title(self):
        self.switchScreen('title')
        display.fill((100, 255, 255))
        screen.print()

    def play(self):
        self.switchScreen('play')
        display.fill((100, 255, 255))
        screen.print()

    def join(self, phase = 0):
        if phase == 0:
            self.switchScreen('join')
            display.fill((255, 255, 0))
            screen.print()
        elif phase == 1:
            self.phase = 1
            self.dim()
            screen.print()

    def name(self):
        self.switchScreen('name')
        display.fill((255, 255, 0))
        screen.print()

    def lobby(self, phase = 0):
        if phase == 0:
            self.switchScreen('lobby')
            display.fill((255, 140, 140))
            screen.print()
        elif phase == 1:
            self.phase = 1
            self.dim()
            screen.print()

    def print(self):
        for widget in self.active_widgets.values():
            if widget[1] == self.phase:
                widget[0].print()

    def getWidget(self, screen, name):
        return self.screens[screen][name][0]

#Images
class Image:
    def __init__(self, filename, pos, ignore_center = False):
        self.image = pygame.image.load(filename)
        self.dimensions = self.image.get_size()
        self.ignore_center = ignore_center
        self.position(pos, ignore_center)

    def position(self, pos, ignore_center):
        if ignore_center:
            self.image_rect = (pos[0], pos[1], self.image.get_width(), self.image.get_height())
        else:
            self.image_rect = self.image.get_rect()
            self.image_rect.center = pos
            self.center = pos

    def getPixel(self, coords):
        pixel = self.image.get_at(coords)
        return (pixel[0], pixel[1], pixel[2])

    def setPixel(self, coords, value):
        self.image.set_at(coords, pygame.Color(value[0], value[1], value[2]))

    def print(self):
        display.blit(self.image, self.image_rect)

class Client(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.ID = None
        self.name = None
        self.avatar = None

    def send(self, message_type, message, raw=False):
        if raw:
            super().send(bytes(json.dumps((message_type, message))+'\uFFFF','utf-8'))
        else:
            super().send(bytes(json.dumps((message_type, ''.join(message.split('\uFFFF'))))+'\uFFFF','utf-8')) 

    def receive(self):
        try:
            m = self.recv(2048)
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

        except socket.timeout:
            return None

    async def clientLoop():
        while True:
            data = self.receive()
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
                
            await asyncio.sleep(0.1)

def compress(rgbarray):
    r = [str(int(i*255)) for i in rgbarray[:-1]]
    r = ''.join(r)
    return r

def decompress(rbgvalue):
    return (int(rgbvalue[:3]),int(rgbvalue[3:6]),int(rgbvalue[6:]),255)

pygame_keys = {pygame.K_0:'0', pygame.K_1:'1', pygame.K_2:'2', pygame.K_3:'3', pygame.K_4:'4', pygame.K_5:'5',
              pygame.K_6:'6', pygame.K_7:'7', pygame.K_8:'8', pygame.K_9:'9', pygame.K_a:'a', pygame.K_b:'b',
              pygame.K_c:'c', pygame.K_d:'d', pygame.K_e:'e', pygame.K_f:'f', pygame.K_g:'g', pygame.K_h:'h',
              pygame.K_i:'i', pygame.K_j:'j', pygame.K_k:'k', pygame.K_l:'l', pygame.K_m:'m', pygame.K_n:'n',
              pygame.K_o:'o', pygame.K_p:'p', pygame.K_q:'q', pygame.K_r:'r', pygame.K_s:'s', pygame.K_t:'t',
              pygame.K_u:'u', pygame.K_v:'v', pygame.K_w:'w', pygame.K_x:'x', pygame.K_y:'y', pygame.K_z:'z',
              pygame.K_SPACE:' ', pygame.K_PERIOD:'.', pygame.K_SEMICOLON:';', pygame.K_SLASH:'/', pygame.K_COMMA:',',
              pygame.K_HASH:'#', pygame.K_QUOTE:"'"}

#mouse
mouse = Mouse()

#screen
screen = Screen()

#set screen to title screen
screen.title()

#clock
clock = pygame.time.Clock()

#Client Socket
client = Client()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #title screen loop
    if screen.current_screen == 'title':
        if mouse.click(screen.getWidget('title', 'play')):
            screen.play()
        elif mouse.click(screen.getWidget('title', 'quit')):
            pygame.quit()
            quit()

    #play screen loop
    elif screen.current_screen == 'play':
        if mouse.click(screen.getWidget('play', 'host')):
            print('Host')
        elif mouse.click(screen.getWidget('play', 'join')):
            screen.join()
        elif mouse.click(screen.getWidget('play', 'back')):
            screen.title()

    elif screen.current_screen == 'join':
        if screen.phase == 0:
            if mouse.clickScreen():
                if screen.using.__class__ == Entry:
                    screen.using.highlight(False)
                screen.using = None

            if mouse.click(screen.getWidget('join', 'ip')):
                screen.using = screen.getWidget('join', 'ip')
                screen.getWidget('join', 'ip').highlight(True)

            elif mouse.click(screen.getWidget('join', 'port')):
                screen.using = screen.getWidget('join', 'port')
                screen.getWidget('join', 'port').highlight(True)

            if mouse.click(screen.getWidget('join', 'back')):
                screen.play()

            elif mouse.click(screen.getWidget('join', 'join')):
                try:
                    IP_Address = screen.getWidget('join', 'ip').raw_text
                    Port = int(screen.getWidget('join', 'port').raw_text)
                    client.connect((IP_Address, Port))
                    screen.name()
                except Exception as e:
                    screen.join(1)
                    print(e)

            elif mouse.click(screen.getWidget('join', 'auto')):
                #automatic connection
                try:
                    with open('server.txt') as f:
                        data = f.read().split('\n')
                        IP_Address = data[0]
                        Port = int(data[1])
                        client.connect((IP_Address, Port))
                        screen.name()
                except Exception as e:
                    screen.join(1)
                    print(e)

        elif screen.phase == 1:
            if mouse.click(screen.getWidget('join', 'ok')):
                screen.join(0)

    elif screen.current_screen == 'name':
        if mouse.clickScreen():
            if screen.using.__class__ == Entry:
                screen.using.highlight(False)
            screen.using = None

        if mouse.click(screen.getWidget('name', 'name')):
            screen.using = screen.getWidget('name', 'name')
            screen.getWidget('name', 'name').highlight(True)

        if mouse.click(screen.getWidget('name', 'back')):
            client.close()
            screen.join()

        elif mouse.click(screen.getWidget('name', 'go')):
            name = screen.getWidget('name', 'name').raw_text
            client.send('N', name)
            profile_image = pygame.image.load('profile.png')
            profile_image = pygame.transform.scale(profile_image, (32,32))
            string_profile = []
            at_line = []
            for x in range(32):
                for y in range(32):
                    at_line.append(compress(profile_image.get_at((x,y)).normalize()))
                string_profile.append(at_line)
                at_line = []
            client.send('I', string_profile)
            print("Sent {}!".format(string_profile))

            screen.lobby(0)

    elif screen.current_screen == 'lobby':
        if screen.phase == 0:
            screen.getWidget('lobby', 'player1').setText('no u')
            if mouse.click(screen.getWidget('lobby', 'leave')):
                screen.getWidget('lobby', 'player1').setColour((0, 0, 255), (255, 255, 255), (255, 255, 0))
                screen.lobby(1)

        elif screen.phase == 1:
            if mouse.click(screen.getWidget('lobby', 'yes')):
                client.close()
                screen.join()
            elif mouse.click(screen.getWidget('lobby', 'no')):
                screen.getWidget('lobby', 'player1').setColour((255, 0, 0), (0, 255, 255), (0, 255, 0))
                screen.lobby(0)

    if screen.using.__class__ == Entry:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in pygame_keys:
                    screen.using.newCharacter(pygame_keys[event.key])
                elif event.key == pygame.K_BACKSPACE:
                    screen.using.newCharacter(None)


    clock.tick(100)
    pygame.display.update()
    mouse.update()
    await asyncio.sleep(0.1)
