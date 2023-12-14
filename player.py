from cmu_graphics import *
import math
from PIL import Image

class Player:
    def __init__(self, x, y, img):
        # Position
        self.x = x
        self.y = y
        
        # Velocity 
        self.dx = 0
        self.dy = 1

        # Acceleration
        self.ddx = 0
        self.g = 10/120
        self.ddy = self.g

        self.radius = 25
        self.angle = None
        self.omega = None
        # image 
        self.img = img

    def draw(self):
        spriteAngle = 0 
        spriteImg = self.img 

        # freefall
        if self.angle == None:
            spriteAngle = 0
            spriteImg = self.img            

        elif self.angle and self.omega: 
            if self.omega < 0:
                spriteImg = self.img.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                spriteImg = self.img
            spriteAngle = 90 - self.angle 
            
        spriteImg = CMUImage(spriteImg)

        drawImage(spriteImg, self.x - self.radius/0.77, self.y-self.radius/0.77, 
                  width = 2*self.radius/0.77, height = 2*self.radius/0.77, 
                  rotateAngle = math.degrees(spriteAngle))
        
        #drawCircle(self.x, self.y, self.radius, fill = None, border = 'red')

    def distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**2)**0.5
    
    def angleToPivot(self, pivot):
        if self.y - pivot.y < 0:
            angle = 2*math.pi + math.atan2((self.y - pivot.y), (pivot.x - self.x))
            return angle
        return math.atan2((self.y - pivot.y), (pivot.x - self.x))
    
    def nearestPivot(self, pivots):
        result = pivots[0]
        closestDistance = self.distance(pivots[0].x, pivots[0].y)
        for i in range(1, len(pivots)):
            pivot = pivots[i]
            pivotDistance = self.distance(pivot.x, pivot.y)
            if  pivotDistance < closestDistance:
                result = pivot
                closestDistance = pivotDistance
        return result

    def swing(self, pivot, r, isScrolling, scrollSpeed, damping = 0):
        
        dt = 1
        self.omega += self.g*math.cos(self.angle) *dt / r - damping*self.omega
        self.angle += self.omega * dt
        
        self.y = pivot.y + r*math.sin(self.angle)
        if not isScrolling:
            self.x = pivot.x - r * math.cos(self.angle) - scrollSpeed
        else:
            self.x = pivot.x - r * math.cos(self.angle)
        v = self.omega * r

        self.dx = v * math.sin(self.angle)
        self.dy = v * math.cos(self.angle)  

    def fall(self, isScrolling, scrollSpeed):
        self.ddy = self.g
        self.ddx = 0
        if not isScrolling:
            self.x += self.dx
        else:
            self.x += self.dx - scrollSpeed
        self.y += self.dy
        self.dx += self.ddx
        self.dy += self.ddy
