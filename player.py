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

        self.radius = 30
        self.ropeLength = None
        self.angle = 0
        self.color = 'green'
        self.omega = None
        # image 
        self.img = img

    def draw(self):
        # print('player:', self.x)
        if self.angle == None:
            angle = 0
        else:
            angle = 90 - self.angle
        if self.angle and math.pi<self.angle < math.pi * 2 :
            img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        else: 
            img = self.img
        img = CMUImage(img)

        drawImage(img, self.x - self.radius, self.y-self.radius, 
                  width = 2*self.radius, height = 2*self.radius, 
                  rotateAngle = math.degrees(angle))
        # drawCircle(self.x, self.y, self.radius, fill = self.color)

    def distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**2)**0.5
    
    def angleToPivot(self, pivot):
        if self.y - pivot.y < 0:
            angle = 2*math.pi + math.atan2((self.y - pivot.y), (pivot.x - self.x))
            return angle
        return math.atan2((self.y - pivot.y), (pivot.x - self.x))
    
    def nearestPivot(self, pivots):
        result = pivots[0]
        result2 = 0
        closestDistance = self.distance(pivots[0].x, pivots[0].y)
        for i in range(1, len(pivots)):
            pivot = pivots[i]
            pivotDistance = self.distance(pivot.x, pivot.y)
            if  pivotDistance < closestDistance:
                result = pivot
                closestDistance = pivotDistance
                result2 = i
        # print(result2)
        return result
    
    # def highestAngle(self, pivot, r):
    #     angle_i = self.angleToPivot(pivot)
    #     # print(math.degrees(angle_i))
    #     KE_i = 0.5 * (self.dx**2 + self.dy**2)
    #     PE_i = -1 * self.g * r * math.sin(angle_i)
    #     E_total = KE_i + PE_i
    #     if E_total >  self.g * r:
    #         return 3/2*math.pi
    #     else:
    #         PE_f = E_total
    #         ratio = PE_f / (-r * self.g)
    #         if ratio < 0:
    #             angle_max = math.pi-math.asin(ratio)
    #         else:
    #             angle_max = math.asin(ratio)
    #         return angle_max

    def swing(self, pivot, r, isScrolling, scrollSpeed):
        
        dt = 1
        self.omega += self.g*math.cos(self.angle) *dt / r - 0.001*self.omega
        self.angle += self.omega * dt
        
        self.y = pivot.y + r*math.sin(self.angle)
        if not isScrolling:
            self.x = pivot.x - r * math.cos(self.angle) - scrollSpeed
        else:
            self.x = pivot.x - r * math.cos(self.angle)
        v = self.omega * r

        self.dx = v * math.sin(self.angle)
        self.dy = v * math.cos(self.angle)


        # self.angle = self.angleToPivot(pivot)
        # v = (self.dx**2 + self.dy**2)**0.5
        # m = 1
        # T = m * v**2 / r + m * self.g * math.sin(self.angle)

        # self.ddy = self.g - T * math.sin(self.angle) / m
        # self.ddx = T * math.cos(self.angle) / m

        # self.dx += self.ddx
        # self.dy += self.ddy

        # self.x += self.dx
        # self.y += self.dy

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
