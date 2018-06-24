import pygame, asyncio, socket

pygame.init()
display = pygame.display.set_mode((250, 250))

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

    def press(self, button):
        button = self.buttons[button]
        if self.pressed[button]:
            return True
        return False

    def click(self, obj, button):
        button = self.buttons[button]
        if self.hover(obj):
            if not self.prev_pressed[button] and self.pressed[button]:
                return True
        return False

    def clickScreen(self, button):
        button = self.buttons[button]
        if not self.prev_pressed[button] and self.pressed[button]:
            return True
        return False

    def hover(self, obj):
        if self.pos[0] in range(obj.rect[0], obj.rect[0] + obj.rect[2]) and self.pos[1] in range(obj.rect[1], obj.rect[1] + obj.rect[3]):
            return True
        return False

    def holding(self, obj):
        if self.hover(obj):
            if self.pressed[0]:
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
    def __init__(self, pos, text, font_size, colour = (255, 200, 100), font_colour = (0, 0, 0)):
        self.colour = colour
        self.formatted_font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = self.formatted_font.render(text, True, font_colour)
        self.font_size = font_size
        self.position(pos)
    def position(self, pos):
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.center = pos
        self.rect = (self.text_rect[0] - self.font_size, self.text_rect[1] - self.font_size, self.text_rect[2] + self.font_size * 2, self.text_rect[3] + self.font_size * 2)
    def print(self):
        pygame.draw.rect(display, self.colour, self.rect)
        display.blit(self.text, self.text_rect)

#mouse
mouse = Mouse()

#buttons
button = Button((125, 200), 'TEST', 20)

clock = pygame.time.Clock()
colours = {True:(0, 255, 0), False:(255, 0, 0)}


print('click, clickScreen, hover, holding, dragging')
while True:
    display.fill((255, 255, 255))
    pygame.event.get()
    pygame.draw.circle(display, colours.get(mouse.press('left')), (25, 25), 20)
    pygame.draw.circle(display, colours.get(mouse.press('right')), (25, 75), 20)
    pygame.draw.circle(display, colours.get(mouse.press('middle')), (25, 125), 20)

    pygame.draw.circle(display, colours.get(mouse.click(button, 'left')), (75, 25), 20)
    pygame.draw.circle(display, colours.get(mouse.click(button, 'right')), (75, 75), 20)
    pygame.draw.circle(display, colours.get(mouse.click(button, 'middle')), (75, 125), 20)

    pygame.draw.circle(display, colours.get(mouse.clickScreen('left')), (125, 25), 20)
    pygame.draw.circle(display, colours.get(mouse.clickScreen('right')), (125, 75), 20)
    pygame.draw.circle(display, colours.get(mouse.clickScreen('middle')), (125, 125), 20)

    pygame.draw.circle(display, colours.get(mouse.hover(button)), (175, 25), 20)

    pygame.draw.circle(display, colours.get(mouse.holding(button)), (225, 25), 20)

    pygame.draw.circle(display, colours.get(mouse.dragging(button)), (275, 25), 20)

    if mouse.dragging(button):
        button.position((mouse.pos[0] + mouse.drag_offset[0], mouse.pos[1] + mouse.drag_offset[1]))

    button.print()
    pygame.display.update()
    mouse.update()
    clock.tick(50)
