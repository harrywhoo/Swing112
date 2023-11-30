from cmu_graphics import *

class Pivot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 5
        
    def __eq__(self, other):
        return (isinstance(other, Pivot) and 
                (self.x == other.x) and 
                (self.y == other.y))
    
    def draw(self, color = None):
        drawCircle(self.x, self.y, self.r, fill = color, border = 'black')

