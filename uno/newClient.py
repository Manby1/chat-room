import pygame, asyncio, socket

pygame.init()
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

    def clickScreen(self, button='left'):
        button = self.buttons[button]
        if not self.prev_pressed[button] and self.pressed[button]:
            return True
        return False

    def hover(self, obj):
        if self.pos[0] in range(obj.rect[0], obj.rect[0] + obj.rect[2]) and self.pos[1] in range(obj.rect[1], obj.rect[1] + obj.rect[3]):
            return True
        return False

    def holding(self, obj):
        button = self.buttons[button]
        if self.hover(obj) and self.pressed[button]:
                return True
        return False

    def dragging(self, obj):
        if self.click(obj, 'left') and self.holding(obj) and self.is_dragging == None:
            self.is_dragging = obj
            self.drag_offset = (obj.center[0] - self.pos[0], obj.center[1] - self.pos[1])
            return True
        elif self.is_dragging == obj and self.pressed[0]:
            return True
        if self.is_dragging == obj:
            self.is_dragging = None
        return False

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

#screen
class Screen:
    def __init__(self):
        self.currentScreen = None
        self.active_widgets = None

        #title widgets
        title_play = Button((300, 600), 'Play!', 50, 20, (60, 60, 255), colour=(80, 80, 255), font_colour=(180, 180, 220), width = 240, height = 150)
        title_quit = Button((700, 600), 'Quit', 50, 20, (200, 0, 0), colour=(255, 0, 50), font_colour=(255, 220, 220), width = 240, height = 150)
        title_splash = Image('splash.png', (500, 250))

        #play widgets
        play_host = Button((300, 400), 'Host', 55, colour=(0, 0, 0), font_colour=(255, 255, 255), border_size=30, border_colour=(50, 0, 0), width = 240, height = 150)
        play_join = Button((700, 400), 'Join', 55, colour=(0, 255, 0), font_colour=(0, 0, 0), border_size=30, border_colour = (0, 200, 0), width = 240, height = 150)
        play_back = Button((70, 50), 'Back', 20, colour=(0, 0, 0), font_colour=(255, 255, 255))

        #list of screens and their widgets
        self.screens = {'title':{'play':title_play, 'quit':title_quit, 'splash':title_splash},
                        'play':{'host':play_host, 'join':play_join, 'back':play_back}}

    def switchScreen(self, screen):
        self.active_widgets = self.screens[screen]
        self.current_screen = screen

    def title(self):
        self.switchScreen('title')
        display.fill((100, 255, 255))
        screen.print()

    def play(self):
        self.switchScreen('play')
        display.fill((255, 0, 0))
        screen.print()

    def print(self):
        for widget in self.active_widgets.values():
            widget.print()

    def getWidget(self, screen, name):
        return self.screens[screen][name]

#Images
class Image:
    def __init__(self, filename, pos):
        self.image = pygame.image.load(filename)
        self.dimensions = self.image.get_size()
        self.position(pos)

    def position(self, pos):
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


#mouse
mouse = Mouse()

#screen
screen = Screen()

#set screen to title screen
screen.title()

while True:
    pygame.event.get()

    #title screen loop
    if screen.current_screen == 'title':
        if mouse.click(screen.getWidget('title', 'play')):
            screen.play()
        elif mouse.click(screen.getWidget('title', 'quit')):
            pygame.quit()
            quit()

    #next screen loop
    elif screen.current_screen == 'play':
        if mouse.click(screen.getWidget('play', 'host')):
            print('Host')
        elif mouse.click(screen.getWidget('play', 'join')):
            print('Join')
        elif mouse.click(screen.getWidget('play', 'back')):
            screen.title()

    pygame.display.update()
    mouse.update()
