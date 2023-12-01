from cmu_graphics import *

class Pivot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 6
        self.originalX = x
        
    def __eq__(self, other):
        return (isinstance(other, Pivot) and 
                (self.x == other.x) and 
                (self.y == other.y))
    
    # def draw(self, scrollX, color = None):
        
    #     cx = self.x
    #     cx -= scrollX
    #     drawCircle(cx, self.y, self.r, fill = color, border = 'black')
    #     print(f'(x,y) = ({self.x}, {self.y})')

    def draw(self, color = None):
        
        drawCircle(self.x, self.y, self.r, fill = color, border = 'black')
        # print(f'(x,y) = ({self.x}, {self.y})')

