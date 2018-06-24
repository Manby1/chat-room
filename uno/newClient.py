import pygame, asyncio, socket

pygame.init()
display = pygame.display.set_mode((1000, 800))

#mouse obj
class Mouse:
    def __init__(self):
        self.pressed = p.mouse.get_pressed()
        self.update()
        self.isDragging = None

    def update(self):
        self.pos = p.mouse.get_pos()
        self.prevPressed = self.pressed
        self.pressed = p.mouse.get_pressed()

    def click(self, obj, button):
        if obj.rect[0] <= self.pos[0] <= obj.rect[0] + obj.rect[2] and obj.rect[1] <= self.pos[1] <= obj.rect[1] + obj.rect[3]:
            if not self.prevPressed[button] and self.pressed[button]:
                return True
        return False

    def clickScreen(self, button):
        if not self.prevPressed[button] and self.pressed[button]:
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
        if self.click(obj, 0) and self.holding(obj) and self.isDragging == None:
            self.isDragging = obj
            self.dragOffset = (obj.rect.center[0] - self.pos[0], obj.rect.center[1] - self.pos[1])
            return True
        elif self.isDragging == obj and self.pressed[0]:
            return True
        if self.isDragging == obj:
            self.isDragging = None
        return False

#gui button
class Button:
    def __init__(self, pos, text, fontSize, colour = (255, 200, 100), fontColour = (0, 0, 0)):
        self.colour = colour
        self.formattedFont = pygame.font.Font('freesansbold.ttf', fontSize)
        self.text = self.formattedFont.render(text, True, fontColour)
        self.textRect = self.text.get_rect()
        self.textRect.center = pos
        self.rect = (self.textRect[0]-fontSize, self.textRect[1]-fontSize, self.textRect[2]+fontSize*2, self.textRect[3]+fontSize*2)
    def print(self):
        pygame.draw.rect(display, self.colour, self.rect)
        display.blit(self.text, self.textRect)

while True:
    pygame.display.update()
    mouse.update()
