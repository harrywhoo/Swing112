from cmu_graphics import *

class Pivot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 10
        self.originalX = x

    def draw(self, color = None):
        drawCircle(self.x, self.y, self.r, fill = color, border = 'black', borderWidth = 4)

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5