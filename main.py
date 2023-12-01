from cmu_graphics import *
from player import *
from pivot import *
from button import *
from wall import *
from spikes import *
from PIL import Image as im
import os, pathlib
import time
import random

def onAppStart(app):
    startGame(app)

def startGame(app):
    # canvas
    app.width = 1000
    app.height = 720
    app.stepsPerSecond = 120
    
    # visuals 
    app.backdrop = openImage("images/background.jpg")
    app.backdropWidth = app.backdrop.width
    app.backdropHeight = app.backdrop.height
    app.backdrop = CMUImage(app.backdrop)

    app.startButton = Button(app.width/2 - 100, app.height/2 - 100, 
                             200, 200, 'start')
    #app.restartButton = 
    
    app.playerImg = openImage("images/playerImg.png")

    app.spikeImg = openImage("images/spike.png")
    app.spikeImg = CMUImage(app.spikeImg)

    app.wallImg = openImage("images/wall.jpg")

    # player 
    app.isSwinging = False
    app.ropeLength = 200
    app.player = Player(app.width*0.4, 100, app.playerImg)

    # pivots
    app.pivots = []
    app.pivots.append(Pivot(app.width/2, app.height/2))
    app.pivots.append(Pivot(app.width*3/4, app.height/2))
    app.pivots.append(Pivot(app.width, app.height/2))
    app.pivots.append(Pivot(app.width*5/4, app.height/2))
    app.pivots.append(Pivot(app.width*3/2, app.height/2))
    app.currPivot = None

    # walls
    app.walls = []
    app.walls.append(Wall(app.width*0.4, app.height*0.8, 100, 50, app.wallImg))
    app.walls.append(Wall(app.width*0.6, app.height*0.4, 100, 200, app.wallImg))
    app.walls.append(Wall(app.width*7/8, app.height*0.8, 100, 50, app.wallImg))
    app.walls.append(Wall(app.width, app.height*0.3, 50, 50, app.wallImg))
    app.walls.append(Wall(app.width*1.2, app.height*0.7, 100, 150, app.wallImg))

    # spikes
    app.spikes = []
    app.spikes.append(Spike(app.width*3/4, app.height*3/4, 30, app.spikeImg))
    app.spikes.append(Spike(app.width*7/8, app.height*0.5, 30, app.spikeImg))
    
    # scrolling 
    app.scrollSpeed = 0
    app.scrollX = 0 
    app.backdropScroll = 0
    app.scrollMargin = 400
    app.isScrolling = False

#--------------------------------- Start ---------------------------------------
def welcome_redrawAll(app):
    app.startButton.draw()

def welcome_onMousePress(app, mouseX, mouseY):
    if app.startButton.clicked(mouseX, mouseY):
        setActiveScreen('game')
        startGame(app)

#--------------------------------- Game ----------------------------------------      
def game_onStep(app):

    # death condition
    if (app.player.y - app.player.radius > app.height or 
        app.player.x - app.player.radius < 0):
        setActiveScreen('death')

    # swinging motion 
    if app.isSwinging:
        # check for wall collision
        if checkWallCollision(app.walls, app.player):
            app.player.omega *= -1 # rebounds player
        elif checkSpikeCollision(app.spikes, app.player):
            app.player.dx = 0
            app.player.dy = 0
            app.player.ddx = 0
            app.player.ddy = 0
            time.sleep(1)
            setActiveScreen('death')
        
        app.player.swing(app.currPivot, app.player.ropeLength, 
                         app.isScrolling, app.scrollSpeed)
        
        makePlayerVisible(app) 
    
    # freefall motion 
    else: 
        # collision with walls
        collision = checkWallCollision(app.walls, app.player)
        if collision in ['left', 'right']:
            app.player.dx *= -1.1
        elif collision in ['top', 'bottom']:
            app.player.dy *= -1.1

        #collision with spikes
        elif checkSpikeCollision(app.spikes, app.player):
            app.player.dx = 0
            app.player.dy = 0
            app.player.ddx = 0
            app.player.ddy = 0
            time.sleep(1)
            setActiveScreen('death')
        
        app.player.fall(app.isScrolling, app.scrollSpeed)

        makePlayerVisible(app)

    updatePositions(app)
    
    removePivots(app)
    removeWalls(app)
    print(len(app.pivots))
    if len(app.pivots)<5:
        generatePivots(app)
    if len(app.walls)<5: 
        generateWalls(app)
    app.player.x -= app.scrollSpeed
    # print(app.player.x)

def game_onKeyPress(app, key):
    if key =='p':
        setActiveScreen('pause')
    
    elif key == 'space':
        app.currPivot = app.player.nearestPivot(app.pivots)
        if canSwing(app.player, app.currPivot, app.ropeLength):
            app.isSwinging = True
            app.player.ropeLength = app.player.distance(app.currPivot.x, 
                                                        app.currPivot.y)
            
            # part of momentum is lost when player initially attaches
            angle = app.player.angleToPivot(app.currPivot)
            app.player.angle = angle
            temp = (app.player.dx * math.sin(angle) + app.player.dy 
                    * math.cos(angle))
            app.player.dx = temp * math.sin(angle)
            app.player.dy = temp * math.cos(angle)
            app.player.omega = temp/app.player.ropeLength        

def game_onKeyRelease(app, key):
    if key == 'space' and app.isSwinging:
        app.isSwinging = False
        app.currPivot = None
        # if app.player.angle < math.pi:
        #     app.player.dy -= 1
        app.player.angle = None

def game_redrawAll(app):
    # drawing backdrop
    numBackdrops = math.ceil(app.width / app.backdropWidth) + 1
    newWidth = app.backdropWidth
    newHeight = app.height
    # print(app.backdropScroll)

    for i in range(numBackdrops):
        drawImage(app.backdrop, i*newWidth - app.backdropScroll, 
                  0, width = newWidth, height = newHeight)

    # Scroll   
    drawLabel(f'app.scrollX = {app.scrollX}', app.width/2, 40, fill='white')

    #player
    app.player.draw()
    # app.player.draw(app.scrollX)

    # pivots
    for pivot in app.pivots:
        if pivot is app.currPivot and app.isSwinging:
            # pivot.draw(app.scrollX, 'blue')
            pivot.draw('blue')
        else: 
            # pivot.draw(app.scrollX)
            pivot.draw()
    # obstacles
    for wall in app.walls:
        wall.draw()
    for spike in app.spikes:
        spike.draw()
    # draw rope
    if app.isSwinging:
        drawLine(app.player.x, app.player.y, app.currPivot.x, app.currPivot.y)

#--------------------------------- Pause ---------------------------------------
def pause_onKeyPress(app, key):
    if key=='p':
        setActiveScreen('game')

def pause_redrawAll(app):
    game_redrawAll(app)
    drawLabel('PAUSED!', app.width/2, 300)

#--------------------------------- Death ---------------------------------------
def death_redrawAll(app):
    drawLabel('YOU DIED!', app.width/2, app.height/2)
    drawLabel('Press r to restart', app.width/2, app.height *0.55)

def death_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('welcome')

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def canSwing(player, currPivot, ropeLength):
    distance = ((player.x - currPivot.x)**2 + (player.y- currPivot.y)**2)**0.5
    return distance <= ropeLength


# Helper functions 

def makePlayerVisible(app):
    # scroll to make player visible as needed
    
    if isScrolling(app): # check to see if player is at margins
        app.isScrolling = True
        app.scrollSpeed = app.player.dx
        app.scrollX += app.scrollSpeed
        app.backdropScroll = app.scrollX % app.backdropWidth
        updatePositions(app)

    # if (app.player.x < app.scrollX + app.scrollMargin):
    #     app.scrollX = app.player.x - app.scrollMargin
    # if (app.player.x > app.scrollX + app.width - app.scrollMargin):
    #     app.scrollX = app.player.x - app.width + app.scrollMargin
    else:
        app.isScrolling = False
        app.scrollSpeed = 0

def checkWallCollision(walls, player):
    for wall in walls:
        collisionSide = wall.collided(player)
        if collisionSide:
            return collisionSide
    return None

def checkSpikeCollision(spikes, player):
    for spike in spikes:
        if spike.collided(player):
            return True
    return False   

def isScrolling(app):
    if (app.player.x > app.width - app.scrollMargin):
        return True
    
def removePivots(app):
    counter = 0
    while counter < len(app.pivots):
        pivot = app.pivots[counter]
        if pivot.x < 0:
            app.pivots.pop(counter)
            print('pivot removed')
        else:
            counter += 1
def removeWalls(app):
    counter = 0
    while counter < len(app.walls):
        wall = app.walls[counter]
        if wall.left + wall.width < 0:
            app.walls.pop(counter)
            print('wall removed')
        else:
            counter += 1
def updatePositions(app):
    for pivot in app.pivots:
        pivot.x -= app.scrollSpeed
    for wall in app.walls:
        wall.left -= app.scrollSpeed
    for spike in app.spikes:
        spike.x -= app.scrollSpeed

def generatePivots(app):
    print('here')
    newPivot = Pivot(randrange(int(1.2*app.width), int(1.3*app.width)), 
                     randrange(int(0.4*app.height), int(0.65 * app.height)))
    app.pivots.append(newPivot)

def generateWalls(app):
    newWall = Wall(app.width*1.4, 
                   randrange(int(app.height*0.3), int(app.height*0.7)), 
                   100, 50, app.wallImg)

# def collided(app):
#     for wall in app.walls:
#         # left side collision
#         if app.player.x + app.player.radius >= wall.left and app.player.y + app.player.radius >= wall.top and app.player.y - app.player.radius <= wall.top + wall.height:
#             return 'left'
#         # right side collision
#         elif app.player.x - app.player.radius <= wall.left + wall.width and app.player.y + app.player.radius >= wall.top and app.player.y - app.player.radius <= wall.top + wall.height:
#             return 'right'
        
#         # top collision
#         elif app.player.x + app.player.radius == wall.left and app.player.x - app.player.radius < wall.left + wall.width and app.player.y + app.player.radius >= wall.top:
#             return 'top'

#         # bottom collision
#         elif app.player.x + app.player.radius == wall.left and app.player.x - app.player.radius < wall.left + wall.width and app.player.y - app.player.radius <= wall.top + wall.height:
#
#              return 'bottom'


# def collision(app):
#     x, y, r = app.player.x, app.player.y, app.player.radius

#     # left collision
#     for wall in app.walls:
#         if x + r <= wall.left and x + app.player.dx + r >= wall.left and y + r >= wall.top and y -r <= wall.top + wall.height:
#             return 'left'
#         elif x - r >= wall.left + wall.width and x + app.player.dx - r <= wall.left + wall.width and y + r >= wall.top and y - r<= wall.top + wall.height:
#             return 'right'
        
#         elif x + r >= wall.left and x - r <= wall.left + wall.width and y + r <= wall.top and y + app.player.dy + r >= wall.top:
#             return 'top'
#         elif x + r >= wall.left and x - r <= wall.left + wall.width and y - r >= wall.top + wall.height and y + app.player.dy - r <= wall.top + wall.height:
#             return 'bottom'
def openImage(fileName):
    return im.open(os.path.join(pathlib.Path(__file__).parent,fileName))

runAppWithScreens(initialScreen='welcome')