from cmu_graphics import *
class Wall:
    def __init__(self, cx, cy, width, height, img):
        self.left = cx - width/2
        self.top = cy - height/2
        self.width = width
        self.height = height
        self.img = img.resize((50, 50))
        self.img = CMUImage(self.img)
    
    def draw(self):
        rows, cols = self.width//50, self.height//50

        for row in range(rows):
            for col in range(cols):
                drawImage(self.img, self.left + 50 * row, 
                          self.top + 50*col, width = 50, height = 50)

    def collided(self, player):
        x, y, r = player.x, player.y, player.radius
        (left, right, top, bottom) = (self.left, self.left + self.width, 
                                      self.top, self.top + self.height)

        # left collision
        if (x + r <= left and x + app.player.dx + r >= left and 
            y + r >= top and y - r <= bottom):
            return 'left'

        # right collision
        elif (x - r >= right and x + app.player.dx - r <= right and 
              y + r >= top and y - r <= bottom):
            return 'right'
        
        # top collision
        elif (y + r <= top and y + app.player.dy + r >= top and 
              x + r >= left and x - r <= right):
            return 'top'

        # bottom collision
        elif (y - r >= bottom and y + app.player.dy - r <= bottom and 
              x + r >= left and x - r <= right):
            return 'bottom'
        # No collision
        return None