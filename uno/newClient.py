import pygame, asyncio, socket

pygame.init()
display = pygame.display.set_mode((1000, 800))

class mouse:
    def __init__(self):
        self.pressed = p.mouse.get_pressed()
        self.update()
        self.isDragging = False

    def update(self):
        self.pos = p.mouse.get_pos()
        self.prevPressed = self.pressed
        self.pressed = p.mouse.get_pressed()

    def click(self, object, button):
        if object.imgRect[0] <= self.pos[0] <= object.imgRect[0] + object.imgRect[2] and object.imgRect[1] <= self.pos[1] <= object.imgRect[1] + object.imgRect[3]:
            if not self.prevPressed[button] and self.pressed[button]:
                return True
        return False

    def clickScreen(self, button):
        if not self.prevPressed[button] and self.pressed[button]:
            return True
        return False

    def hover(self, object):
        if object.imgRect[0] <= self.pos[0] <= object.imgRect[0] + object.imgRect[2] and object.imgRect[1] <= self.pos[1] <= object.imgRect[1] + object.imgRect[3]:
            return True

    def holding(self, object):
        if object.imgRect[0] <= self.pos[0] <= object.imgRect[0] + object.imgRect[2] and object.imgRect[1] <= self.pos[1] <= object.imgRect[1] + object.imgRect[3]:
            if self.pressed[0]:
                return True
        return False

    def dragging(self, object):
        if self.click(object, 0) and self.holding(object) and not self.isDragging:
            self.isDragging = object
            self.dragOffset = (object.imgRect.center[0] - self.pos[0], object.imgRect.center[1] - self.pos[1])
            return True
        elif self.isDragging == object and self.pressed[0]:
            return True
        if self.isDragging == object:
            self.isDragging = False
        return False

class button:
    def __init__(self, pos, text, fontSize, colour = (255, 200, 100), fontColour = (0, 0, 0)):
        self.colour = colour
        self.formattedFont = pygame.font.Font('freesansbold.ttf', fontSize)
        self.text = self.formattedFont.render(text, True, fontColour)
        self.textRect = self.text.get_rect()
        self.textRect.center = pos
        self.rectangleCoords = (self.textRect[0]-fontSize, self.textRect[1]-fontSize, self.textRect[2]+fontSize*2, self.textRect[3]+fontSize*2)

def printButton(button):
    pygame.draw.rect(display, button.colour, button.rectangleCoords)

while True:
    pygame.display.update()
    mouse.update()