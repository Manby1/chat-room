import pygame, asyncio, socket

pygame.init()
display = pygame.display.set_mode((1000, 800))

#mouse obj
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

#gui button
class Button:
    def __init__(self, pos, text, font_size, border_size = 0, border_colour = (0, 0, 0), colour = (255, 200, 100), font_colour = (0, 0, 0)):
        self.colour = colour
        self.border_size = border_size
        self.border_colour = border_colour
        self.formatted_font = pygame.font.Font('Login.ttf', font_size)
        self.text = self.formatted_font.render(text, True, font_colour)
        self.font_size = font_size

        self.position(pos)
    def position(self, pos):
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.center = pos
        self.rect = (self.text_rect[0] - self.font_size, self.text_rect[1] - self.font_size, self.text_rect[2] + self.font_size * 2, self.text_rect[3] + self.font_size * 2)
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
        title_begin = Button((500, 400), 'Uno', 50, 20, (0, 0, 255), colour=(80, 80, 255), font_colour=(180, 180, 220))

        #next widgets
        next_rart = Button((500, 400), 'RART', 75, colour=(0, 0, 0), font_colour=(255, 255, 255), border_size=30, border_colour=(50, 0, 0))
        next_back = Button((60, 50), 'Back', 20, colour=(0, 0, 0), font_colour=(255, 255, 255))

        #list of screens and their widgets
        self.screens = {'title':{'begin':title_begin}, 'next':{'rart':next_rart, 'back':next_back}}

    def switchScreen(self, screen):
        self.active_widgets = self.screens[screen]
        self.current_screen = screen

    def title(self):
        self.switchScreen('title')
        display.fill((100, 255, 255))
        screen.print()

    def next(self):
        self.switchScreen('next')
        display.fill((255, 0, 0))
        screen.print()

    def print(self):
        for widget in self.active_widgets.values():
            widget.print()

    def getWidget(self, screen, name):
        return self.screens[screen][name]

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
        if mouse.click(screen.getWidget('title', 'begin')):
            screen.next()

    #next screen loop
    elif screen.current_screen == 'next':
        if mouse.click(screen.getWidget('next', 'rart')):
            print('Rart!')
        elif mouse.click(screen.getWidget('next', 'back')):
            screen.title()

    pygame.display.update()
    mouse.update()
