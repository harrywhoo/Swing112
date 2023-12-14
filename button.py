from cmu_graphics import *
class Button:
    def __init__(self, left, top, width, height, type):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.type = type
    
    def draw(self, img):
        img = CMUImage(img)
        drawImage(img, self.left, self.top, width = self.width, height = self.height)

    def clickedOrHovered(self, mouseX, mouseY):
        if self.type == 'rectangle':
            return (self.left <= mouseX <= self.left + self.width and 
                    self.top <= mouseY <= self.top + self.height)
        elif self.type == 'circle':
            return distance(self.left+self.width/2, self.top + self.height/2, mouseX, mouseY) <= self.width/2
        
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
