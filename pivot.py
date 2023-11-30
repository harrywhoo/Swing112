from cmu_graphics import *

class Pivot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 5
        self.originalX = x
        
    def __eq__(self, other):
        return (isinstance(other, Pivot) and 
                (self.x == other.x) and 
                (self.y == other.y))
    
    def draw(self, scrollX, color = None):
        cx = self.x
        cx -= scrollX
        drawCircle(cx, self.y, self.r, fill = color, border = 'black')

