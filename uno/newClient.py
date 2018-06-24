import pygame, asyncio, socket

pygame.init()
display = pygame.display.set_mode((1000, 800))

#mouse obj
class Mouse:
    def __init__(self):
        self.pressed = p.mouse.get_pressed()
        self.update()
        self.is_dragging = None

    def update(self):
        self.pos = p.mouse.get_pos()
        self.prev_pressed = self.pressed
        self.pressed = p.mouse.get_pressed()

    def click(self, obj, button):
        if obj.rect[0] <= self.pos[0] <= obj.rect[0] + obj.rect[2] and obj.rect[1] <= self.pos[1] <= obj.rect[1] + obj.rect[3]:
            if not self.prev_pressed[button] and self.pressed[button]:
                return True
        return False

    def clickScreen(self, button):
        if not self.prev_pressed[button] and self.pressed[button]:
            return True
        return False

    def hover(self, obj):
        if obj.rect[0] <= self.pos[0] <= obj.rect[0] + obj.rect[2] and obj.rect[1] <= self.pos[1] <= obj.rect[1] + obj.rect[3]:
            return True

    def holding(self, obj):
        if obj.rect[0] <= self.pos[0] <= obj.rect[0] + obj.rect[2] and obj.rect[1] <= self.pos[1] <= obj.rect[1] + obj.rect[3]:
            if self.pressed[0]:
                return True
        return False

    def dragging(self, obj):
        if self.click(obj, 0) and self.holding(obj) and self.is_dragging == None:
            self.is_dragging = obj
            self.drag_offset = (obj.rect.center[0] - self.pos[0], obj.rect.center[1] - self.pos[1])
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
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.rect = (self.text_rect[0]-font_size, self.text_rect[1]-font_size, self.text_rect[2]+font_size*2, self.text_rect[3]+font_size*2)
    def print(self):
        pygame.draw.rect(display, self.colour, self.rect)
        display.blit(self.text, self.text_rect)

#mouse
mouse = Mouse()

#buttons
button = Button((100, 100), 'Hey.', 10)

while True:
    pygame.display.update()
    mouse.update()