from cmu_graphics import *
class Button:
    def __init__(self, left, top, width, height, message):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.message = message
    
    def draw(self):
        drawRect(self.left, self.top, self.width, self.height, fill = 'yellow')
        drawLabel(self.message, self.left + self.width/2, self.top + self.height/2)

    def clicked(self, mouseX, mouseY):
        return (self.left <= mouseX <= self.left + self.width and 
                self.top <= mouseY <= self.top + self.height)
    