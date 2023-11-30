from cmu_graphics import *
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None

    def draw(self):
        drawCircle(self.x, self.y, 5, fill = self.color, border = 'black')