from cmu_graphics import *

class Spike:
    def __init__(self, x, y, r, img):
        self.x = x
        self.y = y
        self.r = r
        self.img = img
        print(self.x, self.y)

    def draw(self):
        drawImage(self.img, self.x-self.r, self.y-self.r, 
                  width = 2*self.r, height = 2*self.r)

    def collided(self, player):
        if (distance(app.player.x, app.player.y, self.x, self.y) <= 
            app.player.radius + self.r):
            print('spiked')
            return True

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5